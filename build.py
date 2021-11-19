from pybuilder.core import use_plugin, init

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.install_dependencies')
use_plugin('python.flake8')
use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('copy_resources')
use_plugin('python.cram')


name = 'afp-resource-maker'
url = 'https://github.com/ImmobilienScout24/afp_resource_maker'
license = 'Apache License 2.0'
default_task = ['clean', 'analyze', 'publish']


@init
def set_properties(project):
    project.build_depends_on('unittest2')
    project.build_depends_on('mock')
    project.build_depends_on('moto')
    project.build_depends_on('webtest')
    project.depends_on('boto')
    project.depends_on('bottle')
    project.depends_on('requests')
    project.depends_on('docopt')
    project.depends_on('yamlreader')
    project.set_property('flake8_include_test_sources', True)
    project.set_property('flake8_break_build', True)
    project.install_file('/var/www/afp-resource-maker/', 'wsgi/api.wsgi')
    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').extend(['wsgi/*'])


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os
    project.set_property('teamcity_output', True)
    project.version = '%s-%s' % (project.version,
                                 os.environ.get('BUILD_NUMBER', 0))
    project.set_property('install_dependencies_index_url',
                         os.environ.get('PYPIPROXY_URL'))
    project.get_property('distutils_commands').append('bdist_rpm')
