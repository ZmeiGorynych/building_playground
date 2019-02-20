from collections import OrderedDict

def get_name_from_epbunch(x):
    if x.key.lower() == 'version':
        return 'Version','key'
    elif 'Name' in x.fieldnames[1] and x.fieldnames[1] != 'Key_Name' \
            and x.__getattr__(x.fieldnames[1])!='': # the first one is 'key'
        return x.__getattr__(x.fieldnames[1]), x.fieldnames[1]
    # elif 'Variable_Name' in x.fieldnames:
    #     return x.Variable_Name, 'Variable_Name'
    else:
        return None,None


# TODO: all this should be based on the actual grammar, but later :)
def get_wrapper(epbunch, fallback_name):
    if epbunch.key == 'Branch':
        return BranchWrapper(epbunch)
    else:
        return EPBunchWrapperGeneric(epbunch, fallback_name)

class EPBunchWrapperParent:
    def __init__(self, epbunch):
        '''
        Main members: references, a dict of references to other objects
        values: a dict of value fields
        masked_fields: list of fieldnames we don't expose
        :param epbunch:
        '''
        self.obj = epbunch
        self.key = epbunch.key
        self.masked_fields = []
        self.references = OrderedDict()
        self.values = OrderedDict()

    # def __getattr__(self, item):
    #     return self.obj.__getattr__(item)

    # def __getitem__(self, item):
    #     return self.obj.__getattr__(item)

    def __str__(self):
        return 'name: ' + self.name + '\n' + str(self.obj)


class EPBunchWrapperGeneric(EPBunchWrapperParent):
    def __init__(self, epbunch, fallback_name=None):
        super().__init__(epbunch)
        self.name, self.name_source = get_name_from_epbunch(epbunch)
        if self.name is None:
            self.name = fallback_name
            self.name_source = None

        fieldnames = [x for x in epbunch.fieldnames if x not in [self.name_source,'key']]

        for fn in fieldnames:
            # TODO: should really be using the grammar to figure out which fields are references
            if 'Name' in fn or 'Layer' in fn: # this field might be referencing other entities, let's look for those
                child_name = epbunch.__getattr__(fn)
                if looks_like_a_valid_name(child_name):
                    # this looks like a reference, add this to the references dict
                    self.references[fn] = child_name

        value_fieldnames = [fn for fn in fieldnames if fn not in self.references.keys()]
        for fn in value_fieldnames:
            self.values[fn] = epbunch.__getattr__(fn)


class BranchWrapper(EPBunchWrapperParent):
    def __init__(self, epbunch):
        super().__init__(epbunch)
        self.name = epbunch.Name
        self.name_source = 'Name'
        i = 1
        this_name = 'Component_' + str(i) + '_Name'
        while this_name in epbunch.fieldnames and len(epbunch.__getattr__(this_name)):
            this_type = 'Component_' + str(i) + '_Object_Type'
            self.references[this_name] = (self.obj.__getattr__(this_type), self.obj.__getattr__(this_name))
            self.masked_fields += [this_type]#,
                                   # 'Component_' + str(i) + '_Inlet_Node_Name', # ignore these as they are also referenced in the child
                                   # 'Component_' + str(i) + '_Outlet_Node_Name'] # ignore these as they are also referenced in the child

            for name in ['Component_' + str(i) + '_Inlet_Node_Name',  'Component_' + str(i) + '_Outlet_Node_Name']:
                self.references[name] = epbunch.__getattr__(name)

            i += 1
            this_name = 'Component_' + str(i) + '_Name'

        ignored_names = ['Name', 'key'] + self.masked_fields + list(self.references.keys())
        for fn in epbunch.fieldnames:
            if fn not in ignored_names:
                this_value = epbunch.__getattr__(fn)
                if len(this_value):
                    self.values[fn] = this_value

        print('done!')

def matches(name, obj):
    assert type(name) in [str, tuple]
    if type(name) == tuple:
        return name[0] == obj.key and name[1] == obj.name
    else:
        return name == obj.name

def looks_like_a_valid_name(x): # rather than a number or a Boolean
    if not type(x) == str:
        return False
    if x.lower() in ['true','false','yes','no']:
        return False
    else:
        try:
            float(x)
            return False
        except:
            return True