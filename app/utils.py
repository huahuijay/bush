xml_content_starting = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE stax SYSTEM "stax.dtd">
<stax>
	<defaultcall function="func_test"/>
	<function name="func_test">
        <sequence>
'''

xml_content = '''            <loop from="0" to="0">
                <testcase name="'TestA'">
                    <sequence>
                        <process>
                            <location>'local'</location>
                            <command>'/usr/bin/python'</command>
                            <parms>'{STAF/Env/HOME}/PycharmProjects/STAF/staf/staf_wrapper/demo.py case1'</parms>
                        </process>
                        <if expr="RC == 0">
                            <tcstatus result="'pass'"/>
                            <else>
                                <tcstatus result="'fail'"/>
                            </else>
                        </if>
                    </sequence>
                </testcase>
            </loop>
'''

xml_content_ending = '''            </sequence>
    </function>
</stax>
'''

import re
import os
from django.conf import settings

tmp_handle_global = None


def generate_xml(task_name, task_cases):
    proj_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(proj_name, 'media/script')
    xml_path = settings.MEDIA_ROOT + settings.CASE_DIR
    xml_name = '.'.join([task_name, 'xml'])
    # cases = Suite.objects.get(id=p_suite).case_set.all()
    xml_location = os.path.join(xml_path, xml_name)
    print xml_location

    if os.path.exists(xml_location):
        os.remove(xml_location)
    with open(xml_location, 'a+') as xml_handle:
        xml_handle.write(xml_content_starting)
        for task_case in task_cases:
            xml_content_towrite = re.sub('''<command>'.*'</command>''', '''<command>'{case.command}'</command>'''.format(case=task_case.case), xml_content)
            xml_content_towrite = re.sub('''<testcase name="'.*'">''', '''<testcase name="'{case.name}'">'''.format(case=task_case.case), xml_content_towrite)
            xml_content_towrite = re.sub('<parms>.*</parms>', "<parms>'{0}/{case.script} {case.param}'</parms>".format(script_path, case=task_case.case), xml_content_towrite)
            xml_handle.write(xml_content_towrite)
        xml_handle.write(xml_content_ending)
