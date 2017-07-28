
## Delivers job

```
qsub test.jobfile
```

## Shows the status of jobs

```
showq -u enricor
```

## Information about job

```
qstat -n -u user
```

## checkjob information about a specific job

```
checkjob jobid
```

## Remove job

```
qdel jobid
```

## Info about expected start and finish time of a specific job

```
showstart jobid
```

## Login worker node (use default python!)

```
pbs_joblogin jobid
```


## Ref:
https://userinfo.surfsara.nl/systems/lisa/usage/batch-usage#heading13