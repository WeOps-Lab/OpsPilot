SALT.MODULES.TEST
Module for running arbitrary tests

salt.modules.test.arg(*args, **kwargs)
Print out the data passed into the function *args and kwargs, this is used to both test the publication data and CLI argument passing, but also to display the information available within the publication data.

Returns:
{"args": args, "kwargs": kwargs}

Return type:
dict

CLI Example:

salt '*' test.arg 1 "two" 3.1 txt="hello" wow='{a: 1, b: "hello"}'
salt.modules.test.arg_clean(*args, **kwargs)
Like test.arg but cleans kwargs of the __pub* items

CLI Example:

salt '*' test.arg_clean 1 "two" 3.1 txt="hello" wow='{a: 1, b: "hello"}'
salt.modules.test.arg_repr(*args, **kwargs)
Print out the data passed into the function *args and kwargs, this is used to both test the publication data and CLI argument passing, but also to display the information available within the publication data.

Returns:
{"args": repr(args), "kwargs": repr(kwargs)}

CLI Example:

salt '*' test.arg_repr 1 "two" 3.1 txt="hello" wow='{a: 1, b: "hello"}'
salt.modules.test.arg_type(*args, **kwargs)
Print out the types of the args and kwargs. This is used to test the types of the args and kwargs passed down to the Minion

Return type:
dict

CLI Example:

salt '*' test.arg_type 1 'int'
salt.modules.test.assertion(assertion)
Assert the given argument

CLI Example:

salt '*' test.assertion False
salt.modules.test.attr_call()
Call grains.items via the attribute

CLI Example:

salt '*' test.attr_call
salt.modules.test.collatz(start)
Execute the collatz conjecture from the passed starting number, returns the sequence and the time it took to compute. Used for performance tests.

CLI Example:

salt '*' test.collatz 3
salt.modules.test.conf_test()
Return the value for test.foo in the minion configuration file, or return the default value

CLI Example:

salt '*' test.conf_test
salt.modules.test.cross_test(func, args=None)
Execute a minion function via the __salt__ object in the test module, used to verify that the Minion functions can be called via the __salt__ module.

CLI Example:

salt '*' test.cross_test file.gid_to_group 0
salt.modules.test.deprecation_warning()
Return True, but also produce two DeprecationWarnings. One by date, the other by the codename - release Oganesson, which should correspond to Salt 3108.

CLI Example:

salt \* test.deprecation_warning
salt.modules.test.echo(text)
Return a string - used for testing the connection

CLI Example:

salt '*' test.echo 'foo bar baz quo qux'
salt.modules.test.exception(message='Test Exception')
Raise an exception

Optionally provide an error message or output the full stack.

CLI Example:

salt '*' test.exception 'Oh noes!'
salt.modules.test.false_()
Always return False

CLI Example:

salt '*' test.false
salt.modules.test.fib(num)
Return the num-th Fibonacci number, and the time it took to compute in seconds. Used for performance tests.

This function is designed to have terrible performance.

CLI Example:

salt '*' test.fib 3
salt.modules.test.get_opts()
Return the configuration options passed to this minion

CLI Example:

salt '*' test.get_opts
salt.modules.test.kwarg(**kwargs)
Print out the data passed into the function **kwargs, this is used to both test the publication data and CLI kwarg passing, but also to display the information available within the publication data.

CLI Example:

salt '*' test.kwarg num=1 txt="two" env='{a: 1, b: "hello"}'
salt.modules.test.missing_func()
salt.modules.test.module_report()
Return a dict containing all of the execution modules with a report on the overall availability via different references

CLI Example:

salt '*' test.module_report
salt.modules.test.not_loaded()
List the modules that were not loaded by the salt loader system

CLI Example:

salt '*' test.not_loaded
salt.modules.test.opts_pkg()
Return an opts package with the grains and opts for this Minion. This is primarily used to create the options used for Master side state compiling routines

CLI Example:

salt '*' test.opts_pkg
salt.modules.test.outputter(data)
Test the outputter, pass in data to return

CLI Example:

salt '*' test.outputter foobar
salt.modules.test.ping()
Used to make sure the minion is up and responding. Not an ICMP ping.

Returns True.

CLI Example:

salt '*' test.ping
salt.modules.test.provider(module)
Pass in a function name to discover what provider is being used

CLI Example:

salt '*' test.provider service
salt.modules.test.providers()
Return a dict of the provider names and the files that provided them

CLI Example:

salt '*' test.providers
salt.modules.test.raise_exception(name, *args, **kwargs)
Raise an exception. Built-in exceptions and those in salt.exceptions can be raised by this test function. If no matching exception is found, then no exception will be raised and this function will return False.

This function is designed to test Salt's exception and return code handling.

CLI Example:

salt '*' test.raise_exception TypeError "An integer is required"
salt '*' test.raise_exception salt.exceptions.CommandExecutionError "Something went wrong"
salt.modules.test.rand_sleep(max=60)
Sleep for a random number of seconds, used to test long-running commands and minions returning at differing intervals

CLI Example:

salt '*' test.rand_sleep 60
salt.modules.test.rand_str(size=9999999999, hash_type=None)
This function has been renamed to test.random_hash. This function will stay to ensure backwards compatibility, but please switch to using the preferred name test.random_hash.

salt.modules.test.random_hash(size=9999999999, hash_type=None)
New in version 2015.5.2.

Changed in version 2018.3.0: Function has been renamed from test.rand_str to test.random_hash

Generates a random number between 1 and size, then returns a hash of that number. If no hash_type is passed, the hash_type specified by the Minion's hash_type config option is used.

CLI Example:

salt '*' test.random_hash
salt '*' test.random_hash hash_type=sha512
salt.modules.test.retcode(code=42)
Test that the returncode system is functioning correctly

CLI Example:

salt '*' test.retcode 42
salt.modules.test.sleep(length)
Instruct the minion to initiate a process that will sleep for a given period of time.

CLI Example:

salt '*' test.sleep 20
salt.modules.test.stack()
Return the current stack trace

CLI Example:

salt '*' test.stack
salt.modules.test.true_()
Always return True

CLI Example:

salt '*' test.true
salt.modules.test.try_(module, return_try_exception=False, **kwargs)
Try to run a module command. On an exception return None. If return_try_exception is set to True, return the exception. This can be helpful in templates where running a module might fail as expected.

Jinja Example:

{% for i in range(0,230) %}
    {{ salt['test.try'](module='ipmi.get_users', bmc_host='172.2.2.'+i)|yaml(False) }}
{% endfor %}
salt.modules.test.tty(*args, **kwargs)
Deprecated! Moved to cmd.tty

CLI Example:

salt '*' test.tty tty0 'This is a test'
salt '*' test.tty pts3 'This is a test'
salt.modules.test.version()
Return the version of salt on the minion

CLI Example:

salt '*' test.version
salt.modules.test.versions()
This function is an alias of versions_report.

Returns versions of components used by salt

CLI Example:

salt '*' test.versions_report
salt.modules.test.versions_information()
Report the versions of dependent and system software

CLI Example:

salt '*' test.versions_information
salt.modules.test.versions_report()
Returns versions of components used by salt

CLI Example:

salt '*' test.versions_report