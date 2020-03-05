import zipfile, plistlib, sys, re

def analyze_ipa_with_plistlib(ipa_path):
    ipa_file = zipfile.ZipFile(ipa_path)
    plist_path = find_plist_path(ipa_file)
    plist_data = ipa_file.read(plist_path)
    plist_root = plistlib.loads(plist_data)
    return print_ipa_info (plist_root)

def find_plist_path(zip_file):
    name_list = zip_file.namelist()
    pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
    for path in name_list:
        m = pattern.match(path)
        if m is not None:
            return m.group()

def print_ipa_info(plist_root):
    return {
        'version_code':plist_root.get('CFBundleVersion'),
        'version_name':plist_root.get('CFBundleShortVersionString')
    }
    #print ('Display Name: %s' % plist_root['CFBundleDisplayName'])
    #print ('Bundle Identifier: %s' % plist_root['CFBundleIdentifier'])
    #print ('Version: %s' % plist_root['CFBundleShortVersionString'])

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print ('Usage: python3 ipaanalyze.py /path/to/ipa')

    ipa_path = args[0]
    analyze_ipa_with_plistlib(ipa_path)