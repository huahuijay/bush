xml_content_starting = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE stax SYSTEM "stax.dtd">
<stax>
	<defaultcall function="func_test"/>
	<function name="func_test">
        <sequence>'''

xml_content = '''            <loop from="0" to="1">
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