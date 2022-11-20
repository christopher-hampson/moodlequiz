import inspect
from sys import displayhook, stdin
from unittest import expectedFailure
import xml.etree.ElementTree as ET
from .question import GradedQuestion
import json
from dataclasses import dataclass, field
from io import StringIO
import traceback
from ..utils import CDATA

@dataclass
class Testcase:
    mark 		: float = field(default=0)
    testcode 	: str = field(default="")
    expected 	: str = field(default="")
    stdin		: str = field(default="")
    extra 		: str = field(default="",repr=False)
    display 	: str = field(default="",repr=False)
    testtype 	: int = field(default=0,repr=False)
    useasexample	: int = field(default=0,repr=False)
    hiderestiffail 	: int = field(default=0,repr=False)

    @property
    def xml(self):
        xml = ET.Element("testcase")
        xml.set('testtype',str(int(self.testtype)))
        xml.set('useasexample',str(int(self.useasexample)))
        xml.set('hiderestiffail',str(int(self.hiderestiffail)))
        xml.set('mark',f"{self.mark:.7f}")

        testcode = ET.Element("testcode")
        txt = ET.SubElement(testcode,"text")
        txt.text = str(self.testcode)
        xml.append(testcode)

        stdin = ET.Element("stdin")
        txt = ET.SubElement(stdin,"text")
        txt.text = str(self.stdin)
        xml.append(stdin)

        expected = ET.Element("expected")
        txt = ET.SubElement(expected,"text")
        txt.text = str(self.expected)
        xml.append(expected)

        extra = ET.Element("extra")
        txt = ET.SubElement(extra,"text")
        txt.text = str(self.extra)
        xml.append(extra)

        display = ET.Element("display")
        txt = ET.SubElement(display,"text")
        txt.text = str(self.display)
        xml.append(display)

        return xml

    def as_dict(self):
        info = {}
        info.set('testtype',str(int(self.testtype)))
        info.set('useasexample',str(int(self.useasexample)))
        info.set('hiderestiffail',str(int(self.hiderestiffail)))
        info.set('mark',f"{self.mark:.7f}")
        return info


@dataclass
class CodeRunner(GradedQuestion):
    _type			        : str = "coderunner"
    coderunnertype			: str = field(default="python3",repr=False)
    prototypetype			: int = field(default=0,repr=False)
    allornothing			: int = field(default=0,repr=False)
    penaltyregime			: int = field(default=0,repr=False)
    precheck				: int = field(default=1,repr=False)
    hidecheck				: int = field(default=0,repr=False)
    showsource				: int = field(default=0,repr=False)
    answerboxlines			: int = field(default=18,repr=False)
    answerboxcolumns		: int = field(default=100,repr=False)
    _answerpreload			: str = field(default="",repr=False,metadata={'name':'answerpreload','property':'_answerpreload_'})
    gloablextra				: str = field(default="",repr=False)
    useace					: str = field(default="",repr=False)
    iscombinatortemplate	: int = field(default=0,repr=False)
    allowmultiplestdins		: str = field(default="",repr=False)
    _answer 				: str = field(default="",repr=False,metadata={'name':'answer','property':'_answer_'})
    validateonsave			: int = field(default=0,repr=False)
    testsplitterre			: str = field(default="",repr=False)
    language				: str = field(default="",repr=False)
    acelang					: str = field(default="",repr=False)
    sandbox					: str = field(default="",repr=False)
    grader					: str = field(default="TemplateGrader",repr=False)
    cputimelimitsecs		: str = field(default="",repr=False)
    memlimitmb				: str = field(default="",repr=False)
    sandboxparams			: str = field(default="",repr=False)
    templateparams			: str = field(default="",metadata={'xml':'cdata'})
    hoisttemplateparams		: int = field(default=1,repr=False)
    templateparamslang		: str = field(default="twig",repr=False)
    templateparamsevalpertry: int = field(default=0,repr=False)
    templateparamsevald		: str = field(default="",metadata={'xml':'cdata'})
    twigall					: int = field(default=1,repr=False)
    uiplugin				: str = field(default="",repr=False)
    uiparameters			: str = field(default="",repr=False)
    attachments				: int = field(default=0,repr=False)
    attachmentsrequired		: int = field(default=0,repr=False)
    maxfilesize				: int = field(default=10240,repr=False)
    filenamesregex			: str = field(default="",repr=False)
    filenamesexplain		: str = field(default="",repr=False)
    displayfeedback			: int = field(default=1,repr=False)
    _resultcolumns			: str = field(default="",metadata={'xml':'cdata','name':'resultcolumns'})
    _template				: str = field(default="",metadata={'xml':'cdata','name':'template','property':'_template_'})
    testcase				: list = field(default_factory=list,metadata={'xml':'list'})


    def __post_init__(self):
        self.testcase = []
        self._template_list = []
        self._answerpreload_list = []
        self._answer_list = []

    def as_dict(self):
        info = super().as_dict()
        info['answer'] = "\n".join(self._answer_list)
        info['answerpreload'] = "\n".join(self._answerpreload_list)
        info['template'] = CDATA("\n".join(self._template_list))

        return info

    @property
    def resultcolumns(self):
        d = {"feedback":"Feedback",'output':'Output'}
        print("#########")
        return json.dumps([(a,b) for (b,a) in d.items()])


    def add_testcase(self,mark,testcode,expected,*args,**kwargs):
        '''Adds a testcase to the list of testcases'''
        T = Testcase(mark,testcode,expected,*args,**kwargs)
        self.testcase.append(T)

    def __extractfunction(self,f):
        '''Internal function that extracts the text of a callable function or returns a string unaltered.'''
        calledby = inspect.stack()[1][3]
        if isinstance(f,str):
            return f
        elif callable(f):
            lines = inspect.getsource(f).split("\n")
            if "@" in lines[0] and calledby in lines[0]:
                lines = lines[1:]
            return "\n".join(lines)
        else:
            raise Exception("Expected a string or callable")

    def answerpreload(self,f):
        '''Can be used as either a method that takes a function as an argument or as a decorator.'''
        f = self.__extractfunction(f)
        self._answerpreload_list.append(f)
        return f

    def answer(self,f):
        '''Can be used as either a method that takes a function as an argument or as a decorator.'''
        f = self.__extractfunction(f)
        self._answer_list.append(f)
        return f

    def template(self,f):
        '''Can be used as either a method that takes a function as an argument or used as a decorator'''
        f = self.__extractfunction(f)
        self._template_list.append(f)
        return f

    class __ContextManagerStore:
        '''Internal class used for constructing Context Managers that store to the parent class'''

        def __init__(self,parent,store_to):
            self.parent = parent
            self.store_to = store_to

        def __enter__(self):
            pass 

        def __exit__(self, _type, value, _traceback):
            stack = traceback.extract_stack() 
            f, last_line = self._get_origin_info(stack)

            # read lines from file
            with open(f,"r") as fin:
                lines = list(fin)

            # fetches scope of CM by looping over all lines starting from the __enter__ call 
            # until indentation is reduced
            store, offset, first_indent = [], 0, None
            while last_line + offset < len(lines):
                line = lines[last_line + offset]
                indent = len(line) - len(line.lstrip())
                if not first_indent: first_indent = indent
                if indent<first_indent: break
                store.append(line[first_indent:])
                offset+=1
            
            # append lines to parent storage
            try:
                getattr(self.parent,self.store_to).append("".join(store))
            except:
                raise KeyError(f"{self.parent.__class__.__name__} does not have attribute '{self.store_to}'")


        def _get_origin_info(self, stack):
            '''Fetches the filename and linenumber of the last __exit__ call'''
            origin = None
            for i, x in enumerate(stack[::-1]):
                if x[2] == '__exit__':
                    origin = stack[::-1][i + 1]
                    return origin[0], origin[1]
            raise Exception("Context Manager failed to exit successfully.")

    def template_block(self):
        '''Returns a context manager class for wrapping template code'''
        return self.__ContextManagerStore(self,"_template_list")

    def answer_block(self):
        '''Returns a context manager class for wrapping answer code'''
        return self.__ContextManagerStore(self,"_answer_list")

    def answerpreload_block(self):
        '''Returns a context manager class for wrapping answerpreload code'''
        return self.__ContextManagerStore(self,"_answerpreload_list")


            