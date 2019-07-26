#!/usr/bin/env python3
import os.path, sys
from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.descriptor import FieldDescriptor as FD;

struct_tmpl = '''
struct {name}
{{
    void parse();

{fields}
}};
'''
field_tmpl = '    {type} {name}; // {number}'

field_type_map = {FD.TYPE_INT32 : 'int32_t', FD.TYPE_STRING : 'std::string'}

def gen_field(field):
    typemap = {FD.TYPE_INT32 : 'int32_t', FD.TYPE_STRING : 'std::string'}
    return field_tmpl.format(name = field.name, type = field_type_map[field.type], number = field.number)
def gen_fields(msg):
    return [gen_field(field) for field in msg.field]
def gen_struct(msg):
    return struct_tmpl.format(name = msg.name, fields = '\n'.join(gen_fields(msg)))
def gen_code(rq, rp):
    for pfile in rq.proto_file:
        hfile = rp.file.add()
        hfile.name = os.path.splitext(pfile.name)[0] + 'View.h';
        hfile.content = ''.join([gen_struct(msg) for msg in pfile.message_type])

# using stderr for debug logging as stdout is used for communication with compiler
sys.stderr.write('Hello from plugin\n')
rq = plugin.CodeGeneratorRequest()
rp = plugin.CodeGeneratorResponse()
rq.ParseFromString(sys.stdin.buffer.read())
gen_code(rq, rp)
sys.stdout.buffer.write(rp.SerializeToString())

