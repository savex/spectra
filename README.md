# spectra

In short use-case way:

- Collect and store info and attributes: processes, files, configs, etc.
- Do it locally or for multiple hosts. Use SSH <-> PIPE <-> Python.
- No RPC or other fancy stuff.
- Do not use additional libs, main goal: as lightweight as possible.
- Do not install anything on remote host.
- Use plug-in idea for resources grouping. I.e. Specific plugin delivers resource data
- Use specific clients for sourcing info. 'Salt Client' as first such resource info source.

# basic use-cases

The whole idea behind this is too keep track (test) of process status and specific file attributes, networks (...etc) being changed or follow specific rules.
For example, you deployed some system that has multiple components and there is a couple of boys and girls supporting it. It is crucial to have all configs intact and all processes run 24/7.

But when there is multiple people around either they do trust each other or they want to be sure that there is no changes in modules or other stuff during previous 'shift'.

So, here is the plan

 - Install spectra,
 - Use 'collect' option to gather all info that is needed to be looked after
 - Use 'inspect' option to test current situation. Mark inspection with `--checkpoint` to say that this is inspection is to be the new 'origin'.
 - Use subsequent executions of 'inspect' option to track the situation
 - Use 'diff' option to see what has changed since last '-nX' times.
 - Use 'report' option to generate fancy trend report

Here is real life example.
Config file changed, but service not restarted as this is production environment and specific maintenance window required. Time passes, things calm down and all is forgotten up to the moment when someone do restarts actual service. And it do not spin up correctly. There is config changes done by someone who is not around and everyone have a bad headache on this.

Thanks for reading! :)