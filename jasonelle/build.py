import os
import json
import collections

from staticjinja import Site


PROJECT_PATH = os.path.dirname(__file__)
OUTPUT_DIR_NAME = 'output'
OUTPUT_PATH = os.path.join(PROJECT_PATH, OUTPUT_DIR_NAME)


def recursive_rename_extension(directory, to_extension):
    dest_ext = '.' + to_extension

    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            # get the path to your file
            orginal_ext = '.' + filename.split('.')[-1]

            file_path = os.path.join(subdir, filename)
            new_file_path = file_path.replace(orginal_ext, dest_ext)
            os.rename(file_path, new_file_path)


def recursive_pretty_json(directory):
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if '.json' not in filename:
                continue

            file_path = os.path.join(subdir, filename)

            json_content = open(file_path, 'r').read()

            parsed = json.loads(
                json_content, object_pairs_hook=collections.OrderedDict
            )
            pretty = json.dumps(parsed, indent=4, sort_keys=False)

            with open(file_path, 'w') as f:
                f.write(pretty)


CONTEXT = {
    'base_url_jason': "http://localhost.com:8080/json-jinja/output",
    'base_url_app': "http://localhost.com:8080",
    'header_title': "MyNewApplication",
    'head_offline': "true",
}


if __name__ == "__main__":

    site = Site.make_site(
        outpath=OUTPUT_PATH,
        contexts=[('.*.', CONTEXT)]
    )
    site.render()

    print("Renaming {0}/*.html to {0}/*.json".format(OUTPUT_DIR_NAME))
    recursive_rename_extension(OUTPUT_PATH, 'json')

    print("Formatting {0}/*.json".format(OUTPUT_DIR_NAME))
    recursive_pretty_json(OUTPUT_PATH)
