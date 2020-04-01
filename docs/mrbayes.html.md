
---
header-includes:
    - \usepackage[most]{tcolorbox}
    - \definecolor{question-bg}{rgb}{1, 0.95, 0.7}
    - \definecolor{note-bg}{rgb}{0.9, 0.9, 1.0}
    - \newtcolorbox{questionquote}{colback=question-bg,grow to right by=-10mm,grow to left by=-10mm, boxrule=0pt,boxsep=0pt,breakable}
    - \newcommand{\questionbox}[1]{\begin{questionquote} \textbf{QUESTION:} \emph{#1} \end{questionquote}}
    - \newtcolorbox{notequote}{colback=note-bg,grow to right by=-10mm,grow to left by=-10mm, boxrule=0pt,boxsep=0pt,breakable}
    - \newcommand{\notebox}[1]{\begin{notequote} \textbf{NOTE:} \emph{#1} \end{notequote}}
    - \newtcolorbox{outputquote}{colback=output-bg,grow to right by=-10mm,grow to left by=-10mm, boxrule=0pt,boxsep=0pt,breakable}
toc: true
title: Bayesian Phylogenetic Inference with MrBayes
---

\notebox{The following lab exercise is copied from Jeet Sukumaran, based on a tutorial written by Paul Lewis.}

# Resources

-   The data files for the lab can be found [here](http://phylo.bio.ku.edu/sisg2014/algaemb.nex).
-   MrBayes is installed on my lab's workstations and is available using the command ``mb``.
-   You can also download MrBayes for your personal machine from [here](http://nbisweden.github.io/MrBayes/).


# A Typical Analysis Using MrBayes

Start the program by typing:

~~~
$ mb
~~~

A typical analysis requires the following steps:

1.  Reading in the data (command **execute**)
2.  Specifying the substitution model (**lset**) and setting up the
    priors (**prset**)
3.  Specifying the MCMC settings (**mcmcp**)
4.  Running the analysis (**mcmc**, the command **mcmcp** is identical
    to **mcmc** except that it does not actually start a run.)
5.  Summarizing the results (**sumt** and **sump**)


# Reading in the Data

Type:

```
execute algaemb.nex
```

# Help!

You can obtain information (including the current settings) by typing
**help** followed by the command name: for example,

```
help lset
```

Commands in MrBayes are (intentionally) similar to those in PAUP\*, but
the differences can be frustrating. For instance, **lset ?** in PAUP\*
gives you information about the current likelihood settings, but this
does not work in MrBayes. Also, the **lset** command in MrBayes has many
options not present in PAUP\*, and vice versa. Get used to typing
**help** followed by the name of a command in MrBayes to see what
options are allowed for a particular command.

### [ Specifying the model ]{#Specifying_the_model .mw-headline}

The command

```
showmodel
```

prints the current model setting to the screen. In my case this looks
like this

+-----------------------------------------------------------------------+
| **MrBayes screen output:**                                            |
| ``` {style="font-size: 1.25em"}                                       |
|    Model settings:                                                    |
|                                                                       |
|       Data not partitioned --                                         |
|          Datatype  = RNA                                              |
|          Nucmodel  = 4by4                                             |
|          Nst       = 1                                                |
|          Covarion  = No                                               |
|          # States  = 4                                                |
|                      State frequencies have a Dirichlet prior         |
|                      (1.00,1.00,1.00,1.00)                            |
|          Rates     = Equal                                            |
|                                                                       |
|    Active parameters:                                                 |
|                                                                       |
|       Parameters                                                      |
|       ------------------                                              |
|       Statefreq        1                                              |
|       Ratemultiplier   2                                              |
|       Topology         3                                              |
|       Brlens           4                                              |
|       ------------------                                              |
|                                                                       |
|       1 --  Parameter  = Pi                                           |
|             Type       = Stationary state frequencies                 |
|             Prior      = Dirichlet                                    |
|                                                                       |
|       2 --  Parameter  = Ratemultiplier                               |
|             Type       = Partition-specific rate multiplier           |
|             Prior      = Fixed(1.0)                                   |
|                                                                       |
|       3 --  Parameter  = Tau                                          |
|             Type       = Topology                                     |
|             Prior      = All topologies equally probable a priori     |
|             Subparam.  = V                                            |
|                                                                       |
|       4 --  Parameter  = V                                            |
|             Type       = Branch lengths                               |
|             Prior      = Unconstrained:Exponential(10.0)              |
| ```                                                                   |
+-----------------------------------------------------------------------+

Note that **Nst** (number of substitution types) is fixed to one. The
State frequencies are listed as active parameters and, if we started an
analysis with the current settings, would be updated in the MCMC
analysis. Other active parameters are the tree topology and the
associated branch lengths. We can ignore the *Ratemultiplier* parameter.
It is listed here but since we only have one data partition it has no
effect here.

+-----------------------------------------------------------------------+
| -   Which substitution model is currently specified?                  |
|     [Answer]{title="F81" style="border-bottom:1px dotted"}            |
+-----------------------------------------------------------------------+

\
Let's assume we would like a 2-parameter substitution matrix (i.e. the
rate matrix has only two substitution rates, the transition rate and the
transversion rate), and rates to vary across sites according to a gamma
distribution with 4 categories.

```
lset nst=2 rates=gamma ngammacat=4
```

Type

```
showmodel
```

and compare the screen output to before. It should reflect the changes
we have just made to the model.

+-----------------------------------------------------------------------+
| -   Which substitution model is it now? [Answer]{title="HKY+Γ"        |
|     style="border-bottom:1px dotted"}                                 |
+-----------------------------------------------------------------------+

### [ Specifying the priors ]{#Specifying_the_priors .mw-headline}

Now that MrBayes knows which parameters we want in our model, we have to
specify priors for all of them. Type

```
help prset
```

to see a list of the current settings (the list also includes priors
that do not apply to the current analysis).

#### [ Specifying the prior on tree topologies ]{#Specifying_the_prior_on_tree_topologies .mw-headline}

We can see from the previous output that the default prior on topologies
is uniform. This means that the prior probability of any tree topology
is 1/(\# possible topologies for this data set. MrBayes only recognizes
strictly bifurcating topologies.

#### [ Specifying the prior on branch lengths ]{#Specifying_the_prior_on_branch_lengths .mw-headline}

```
prset brlenspr=unconstrained:exp(10.0)
```

The above command specifies that branch lengths are to be unconstrained
(i.e. a molecular clock is not assumed) and the prior distribution to be
applied to each branch length is an exponential distribution with mean
1/10. Note that the value you specify for unconstrained:exp is the
inverse of the mean. (This is also the default setting so the last
command didn't actually change anything.)

#### [ Specifying the prior on the gamma shape parameter ]{#Specifying_the_prior_on_the_gamma_shape_parameter .mw-headline}

```
prset shapepr=exp(1.0)
```

This command specifies an exponential distribution with mean 1.0 for the
shape parameter of the gamma distribution we will use to model rate
heterogeneity.

#### [ Specifying the prior on kappa ]{#Specifying_the_prior_on_kappa .mw-headline}

```
prset tratiopr=beta(1.0,1.0)
```

The command above says to use a Beta(1,1) distribution as the prior for
the transition/transversion rate ratio. You may be thinking that it is a
little strange to use a Beta distribution for a parameter that ranges
from 0 to infinity, and if so you would be right! Allow me to explain as
best I can. Recall that the kappa parameter is the ratio $\alpha$ / $\beta$, where $\alpha$
is the rate of transitions and $\beta$ is the rate of transversions. Rather
than allowing you to place a prior directly on the ratio $\alpha$ / $\beta$, which
ranges from 0 to infinity, MrBayes asks you to instead place a joint
(Beta) prior on $\alpha$ and $\beta$. Here, $\alpha$ and $\beta$ act like $p$ and $1 - p$ in the
familiar coin flipping experiment. The reasoning behind this is
esoteric, but is the same as the reasoning behind the (now commonplace)
use of Dirichlet priors for the GTR relative rates, which is explained
nicely in Zwickl and Holder (2004)^[\[4\]](#cite_note-zwickl2004-3)^.

You might wonder what the Beta(1,1) distribution (figure on the left)
implies about kappa. Transforming the Beta density into the density of $\alpha$
/ $\beta$ results in a density for kappa that is very close, but not
identical, to an exponential(1) distribution. This is known as the [beta
prime
distribution](http://en.wikipedia.org/wiki/Beta_prime_distribution){.external
.text}, and has support (0, infinity), which is appropriate for a ratio
such as kappa. The beta prime distribution is somewhat peculiar,
however, when both parameters are 1 (as they are in this case): in this
case, the mean is not defined, which is to say that we cannot predict
the mean of a sample of kappa values drawn from this distribution. It is
not necessary for a prior distribution to have a well-defined mean, so
this is OK.

#### [ Specifying a prior on base frequencies ]{#Specifying_a_prior_on_base_frequencies .mw-headline}

```
prset statefreqpr=dirichlet(1.0,1.0,1.0,1.0)
```

The above command states that a flat dirichlet distribution is to be
used for base frequencies. The Dirichlet distribution is like the Beta
distribution, except that it is applicable to combinations of
parameters. Like the Beta distribution, the distribution is symmetrical
if all the parameters of the distribution are equal, and the
distribution is flat if all the parameters of the distribution are equal
to 1.0. Using the command above specifies a flat Dirichlet prior, which
says that any combination of base frequencies will be given equal prior
weight. This means that (0.01, 0.99, 0.0, 0.0) is just as probable, a
priori, as (0.25, 0.25, 0.25, 0.25). If you wanted base frequencies to
not stray much from (0.25, 0.25, 0.25, 0.25), you could specify, say,
`statefreqpr=dirichlet(10.0,10.0,10.0,10.0)`
instead.

### [ Specifying MCMC options ]{#Specifying_MCMC_options .mw-headline}

Type

```
help mcmc
```

to view the current MCMC settings. The following options have to do with
calculating a convergence diagnostic during the run. We will modify
these below.

+-----------------------------------------------------------------------+
| **MrBayes screen output:**                                            |
| ``` {style="font-size: 1.25em"}                                       |
|    Mcmcdiagn       Yes/No                Yes                          |
|    Diagnfreq       <number>              5000                         |
|    Diagnstat       Avgstddev/Maxstddev   Avgstddev                    |
|    Minpartfreq     <number>              0.10                         |
|    Allchains       Yes/No                No                           |
|    Allcomps        Yes/No                No                           |
|    Relburnin       Yes/No                Yes                          |
|    Burnin          <number>              0                            |
|    Burninfrac      <number>              0.25                         |
|    Stoprule        Yes/No                No                           |
|    Stopval         <number>              0.05                         |
|                                                                       |
| ```                                                                   |
+-----------------------------------------------------------------------+

Type

```
mcmcp ngen=100000 samplefreq=100 printfreq=1000 nruns=2 nchains=2 stoprule=yes stopval=0.01
```

to specify most of the remaining details of the analysis:

`ngen=100000`{style="font-size: 1.25em"} tells MrBayes that its robots
should each take 100,000 steps. You should ordinarily use much larger
values for ngen than this! We're keeping it small here because we do not
have a lot of time and the purpose of this lab is to learn how to use
MrBayes, not produce a publishable result.
`samplefreq=100`{style="font-size: 1.25em"} says to only save parameter
values and the tree topology every 100 steps.
`printfreq=100`{style="font-size: 1.25em"} says that we would like a
progress report to the screen every 1000 steps.

`nruns=2`{style="font-size: 1.25em"} says to do two independent runs
(MrBayes performs two separate analyses by default).

`nchains=2`{style="font-size: 1.25em"} says that we would like to have 2
heated chains running in addition to the cold chain. The default is one
cold chain and three heated chains but this would take to long right
now, because we are all sharing a few processors on the cluster. This
way, MrBayes will run two independent analyses, each with a cold chain
and a single hot chain.

`stoprule=yes`{style="font-size: 1.25em"} tells MrBayes to stop the run
when the average standard deviation of split frequencies has reached a
certain threshold (`stopval=0.01`{style="font-size: 1.25em"}).

### [ Specifying an outgroup ]{#Specifying_an_outgroup .mw-headline}

```
outgroup Anacystis_nidulans
```

This merely affects the display of trees. It says we want trees to be
rooted between the taxon Anacystis\_nidulans and everything else.

### [ Running the analysis ]{#Running_the_analysis .mw-headline}

We are now ready to start the run by typing

```
mcmc
```

While MrBayes runs, it shows one-line progress reports. The first column
is the step number. The next two columns show the log-likelihoods of the
separate chains that are running, with the cold chain indicated by
square brackets rather than parentheses. The asterisk separates the
screen output for the two independent analyses. The last complete column
is a prediction of the time remaining until the run completes. The
columns consisting of only -- are simply separators, they have no
meaning.

When I tried this, the analysis hit the stop value after 40,000
generations:

+--------------------------------------------------------------------------+
| **MrBayes screen output:**                                               |
| ``` {style="font-size: 1.25em"}                                          |
|    36000 -- [-3180.322] (-3180.202) * [-3179.141] (-3180.397) -- 0:00:21 |
|    37000 -- [-3180.560] (-3181.537) * (-3182.427) [-3178.440] -- 0:00:20 |
|    38000 -- (-3185.505) [-3176.655] * (-3177.682) [-3182.832] -- 0:00:19 |
|    39000 -- (-3180.690) [-3179.084] * [-3181.647] (-3185.312) -- 0:00:20 |
|    40000 -- [-3178.379] (-3179.759) * [-3177.612] (-3183.339) -- 0:00:19 |
|                                                                          |
|    Average standard deviation of split frequencies: 0.007048             |
|                                                                          |
|    Analysis stopped because convergence diagnostic hit stop value.       |
|                                                                          |
|    Analysis completed in 13 seconds                                      |
|    Analysis used 12.78 seconds of CPU time                               |
| ```                                                                      |
+--------------------------------------------------------------------------+

MrBayes will then report various statistics about the run, such as the
percentage of time it was able to accept proposed changes of various
sorts. These percentages should, ideally, all be between about 20% and
40%, but as long as they are not extreme (e.g. 1% or 99%) then things
went well.

Note the section of the output labeled Acceptance rates for moves in the
"cold" chain. This gives the proportion of the time that proposals for
various parameters were accepted:

In my case this was

+-----------------------------------------------------------------------+
| **MrBayes screen output:**                                            |
| ``` {style="font-size: 1.25em"}                                       |
|    Acceptance rates for the moves in the "cold" chain of run 1:       |
|       With prob.   (last 100)   chain accepted proposals by move      |
|          33.7 %     ( 35 %)     Dirichlet(Tratio)                     |
|          24.8 %     ( 21 %)     Dirichlet(Pi)                         |
|          30.3 %     ( 31 %)     Slider(Pi)                            |
|          46.1 %     ( 44 %)     Multiplier(Alpha)                     |
|           7.6 %     ( 12 %)     ExtSPR(Tau,V)                         |
|           2.5 %     (  1 %)     ExtTBR(Tau,V)                         |
|          10.1 %     ( 10 %)     NNI(Tau,V)                            |
|          10.5 %     ( 16 %)     ParsSPR(Tau,V)                        |
|          33.9 %     ( 24 %)     Multiplier(V)                         |
|          28.5 %     ( 34 %)     Nodeslider(V)                         |
|                                                                       |
|    Acceptance rates for the moves in the "cold" chain of run 2:       |
|       With prob.   (last 100)   chain accepted proposals by move      |
|          32.6 %     ( 32 %)     Dirichlet(Tratio)                     |
|          25.3 %     ( 25 %)     Dirichlet(Pi)                         |
|          31.8 %     ( 26 %)     Slider(Pi)                            |
|          48.1 %     ( 50 %)     Multiplier(Alpha)                     |
|           8.0 %     ( 13 %)     ExtSPR(Tau,V)                         |
|           2.3 %     (  2 %)     ExtTBR(Tau,V)                         |
|           9.2 %     ( 13 %)     NNI(Tau,V)                            |
|          10.2 %     ( 10 %)     ParsSPR(Tau,V)                        |
|          33.7 %     ( 22 %)     Multiplier(V)                         |
|          27.4 %     ( 18 %)     Nodeslider(V)                         |
| ```                                                                   |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| -   What explanation could you offer if the acceptance rate was very  |
|     low, e.g. 1%? [Answer]{title="Proposal step-size too big"         |
|     style="border-bottom:1px dotted"}                                 |
| -   What explanation could you offer if the acceptance rate was very  |
|     high, e.g. 99%? [Answer]{title="Proposal step-size too small"     |
|     style="border-bottom:1px dotted"}                                 |
+-----------------------------------------------------------------------+

In the above table, 46.1% (in run 1, in run 2 it was 48.1%) of proposals
to change the gamma shape parameter were accepted. This makes it sounds
as if the gamma shape parameter was changed quite often, but to get the
full picture, you need to scroll up to the beginning of the output and
examine this section:

+-----------------------------------------------------------------------+
| **MrBayes screen output:**                                            |
| ``` {style="font-size: 1.25em"}                                       |
|    The MCMC sampler will use the following moves:                     |
|       With prob.  Chain will use move                                 |
|          2.08 %   Dirichlet(Tratio)                                   |
|          1.04 %   Dirichlet(Pi)                                       |
|          1.04 %   Slider(Pi)                                          |
|          2.08 %   Multiplier(Alpha)                                   |
|         10.42 %   ExtSPR(Tau,V)                                       |
|         10.42 %   ExtTBR(Tau,V)                                       |
|         10.42 %   NNI(Tau,V)                                          |
|         10.42 %   ParsSPR(Tau,V)                                      |
|         41.67 %   Multiplier(V)                                       |
|         10.42 %   Nodeslider(V)                                       |
| ```                                                                   |
+-----------------------------------------------------------------------+

This says that an attempt to change the gamma shape parameter will only
be made in 2.08% of the iterations. That means, out of 40,000 iterations
(called generations by MrBayes), only about 832 attempts were made to
change the gamma shape parameter, and in run one 46.1% of those, or
about 383, were accepted. If you were keenly interested in the posterior
distribution of the gamma shape parameter, you would probably want to
base this on more values (you could also check the ESS with Tracer).

This brings up a couple of important points. First, in each iteration,
MrBayes chooses a move at random to try. Each move is associated with a
"proposal rate" (*Rel. prob*). The proposal rates can be listed using
the

```
showmoves
```

command (**note:** this command is called props in **version 3.1.2**,
where it shows a list of all possible moves). The output will be
something like this:

+-----------------------------------------------------------------------+
| **MrBayes screen output:**                                            |
| ``` {style="font-size: 1.25em"}                                       |
|    Moves that will be used by MCMC sampler (rel. proposal prob. > 0.0 |
| ):                                                                    |
|                                                                       |
|       1 -- Move        = Dirichlet(Tratio)                            |
|            Type        = Dirichlet proposal                           |
|            Parameter   = Tratio [param. 1] (Transition and transversi |
| on rates)                                                             |
|            Tuningparam = alpha (Dirichlet parameter)                  |
|                  alpha = 47.088  [run 1, chain 1]                     |
|                          46.620  [run 1, chain 2]                     |
|                          47.088  [run 2, chain 1]                     |
|                          46.156  [run 2, chain 2]                     |
|            Targetrate  = 0.250                                        |
|            Rel. prob.  = 1.0                                          |
|                                                                       |
|       2 -- Move        = Dirichlet(Pi)                                |
|            Type        = Dirichlet proposal                           |
|            Parameter   = Pi [param. 2] (Stationary state frequencies) |
|            Tuningparam = alpha (Dirichlet parameter)                  |
|                  alpha = 102.020  [run 1, chain 1]                    |
|                          100.000  [run 1, chain 2]                    |
|                          102.020  [run 2, chain 1]                    |
|                          104.081  [run 2, chain 2]                    |
|            Targetrate  = 0.250                                        |
|            Rel. prob.  = 0.5                                          |
|                                                                       |
|       3 -- Move        = Slider(Pi)                                   |
|            Type        = Sliding window                               |
|            Parameter   = Pi [param. 2] (Stationary state frequencies) |
|            Tuningparam = delta (Sliding window size)                  |
|                  delta = 0.208                                        |
|            Targetrate  = 0.250                                        |
|            Rel. prob.  = 0.5                                          |
|                                                                       |
|       4 -- Move        = Multiplier(Alpha)                            |
|            Type        = Multiplier                                   |
|            Parameter   = Alpha [param. 3] (Shape of scaled gamma dist |
| ribution of site rates)                                               |
|            Tuningparam = lambda (Multiplier tuning parameter)         |
|                 lambda = 0.878                                        |
|            Targetrate  = 0.250                                        |
|            Rel. prob.  = 1.0                                          |
|                                                                       |
|       5 -- Move        = ExtSPR(Tau,V)                                |
|            Type        = Extending SPR                                |
|            Parameters  = Tau [param. 5] (Topology)                    |
|                          V [param. 6] (Branch lengths)                |
|            Tuningparam = p_ext (Extension probability)                |
|                          lambda (Multiplier tuning parameter)         |
|                  p_ext = 0.500                                        |
|                 lambda = 0.098                                        |
|            Rel. prob.  = 5.0                                          |
|                                                                       |
|       6 -- Move        = ExtTBR(Tau,V)                                |
|            Type        = Extending TBR                                |
|            Parameters  = Tau [param. 5] (Topology)                    |
|                          V [param. 6] (Branch lengths)                |
|            Tuningparam = p_ext (Extension probability)                |
|                          lambda (Multiplier tuning parameter)         |
|                  p_ext = 0.500                                        |
|                 lambda = 0.098                                        |
|            Rel. prob.  = 5.0                                          |
|                                                                       |
|       7 -- Move        = NNI(Tau,V)                                   |
|            Type        = NNI move                                     |
|            Parameters  = Tau [param. 5] (Topology)                    |
|                          V [param. 6] (Branch lengths)                |
|            Rel. prob.  = 5.0                                          |
|                                                                       |
|       8 -- Move        = ParsSPR(Tau,V)                               |
|            Type        = Parsimony-biased SPR                         |
|            Parameters  = Tau [param. 5] (Topology)                    |
|                          V [param. 6] (Branch lengths)                |
|            Tuningparam = warp (parsimony warp factor)                 |
|                          lambda (multiplier tuning parameter)         |
|                          r (reweighting probability)                  |
|                   warp = 0.100                                        |
|                 lambda = 0.098                                        |
|                      r = 0.050                                        |
|            Rel. prob.  = 5.0                                          |
|                                                                       |
|       9 -- Move        = Multiplier(V)                                |
|            Type        = Random brlen hit with multiplier             |
|            Parameter   = V [param. 6] (Branch lengths)                |
|            Tuningparam = lambda (Multiplier tuning parameter)         |
|                 lambda = 3.657  [run 1, chain 1]                      |
|                          4.042  [run 1, chain 2]                      |
|                          3.549  [run 2, chain 1]                      |
|                          3.883  [run 2, chain 2]                      |
|            Targetrate  = 0.250                                        |
|            Rel. prob.  = 20.0                                         |
|                                                                       |
|      10 -- Move        = Nodeslider(V)                                |
|            Type        = Node slider (uniform on possible positions)  |
|            Parameter   = V [param. 6] (Branch lengths)                |
|            Tuningparam = lambda (Multiplier tuning parameter)         |
|                 lambda = 0.191                                        |
|            Rel. prob.  = 5.0                                          |
|                                                                       |
|    Use 'Showmoves allavailable=yes' to see a list of all available mo |
| ves                                                                   |
| ```                                                                   |
+-----------------------------------------------------------------------+

Summing the five proposal rates yields 1+0.5+0.5+1+5+5+5+5+20+5=48. To
get the probability of using one of these moves in any particular
iteration, MrBayes divides the proposal rate for the move by this sum.
Thus, the gamma shape parameter will be chosen with probability 1/48 =
0.0208, i.e. it will be updated in about 2.08% of the iterations.

Second, note that MrBayes places a lot of emphasis on modifying the tree
topology and branch lengths (in this case 97% of proposals), but puts
little effort (3%) into updating other model parameters. You can change
the percent effort for a particular move using the **props** command.
(**Note:** this is easier to do in version 3.1.2 but version 3.2 gives
you more control, in version 3.2 you can also use the propset command in
batch mode).

The section entitled "Chain swap information" reports the number of
times the cold chain attempted to swap with the heated chain (lower
left) and the proportion of time such attempts were successful (upper
right). The total number of attempted swaps should be the same as the
number of generations, i.e. in this case 40,000.

In my case this was

+-----------------------------------------------------------------------+
| **MrBayes screen output:**                                            |
| ``` {style="font-size: 1.25em"}                                       |
|    Chain swap information for run 1:                                  |
|                                                                       |
|                1      2                                               |
|         ----------------                                              |
|       1 |          0.80                                               |
|       2 |  40000                                                      |
|                                                                       |
|    Chain swap information for run 2:                                  |
|                                                                       |
|                1      2                                               |
|         ----------------                                              |
|       1 |          0.79                                               |
|       2 |  40000                                                      |
|                                                                       |
|    Upper diagonal: Proportion of successful state exchanges between c |
| hains                                                                 |
|    Lower diagonal: Number of attempted state exchanges between chains |
|                                                                       |
|    Chain information:                                                 |
|                                                                       |
|      ID -- Heat                                                       |
|     -----------                                                       |
|       1 -- 1.00  (cold chain)                                         |
|       2 -- 0.91                                                       |
|                                                                       |
|    Heat = 1 / (1 + T * (ID - 1))                                      |
|       (where T = 0.10 is the temperature and ID is the chain number)  |
| ```                                                                   |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| -   Do you see evidence that the 2 chains are swapping with each      |
|     other?                                                            |
|     [Answer]{title="In the example shown here, the chains swapped sta |
| tes successfully 80% of the time in run 1 and 79% of the time in run  |
| 2"                                                                    |
|     style="border-bottom:1px dotted"}                                 |
+-----------------------------------------------------------------------+

### [ Running MrBayes in batch mode ]{#Running_MrBayes_in_batch_mode .mw-headline}

MrBayes does not have to be run interactively. Instead, the commands can
be written in a separate command block in a Nexus file and they will be
executed sequentially. In fact, this is the preferred method of running
an analysis once you are familiar with the commands. A minimal MrBayes
block would be

+-----------------------------------------------------------------------+
| **A minimal MrBayes block:**                                          |
| ``` {style="font-size: 1.25em"}                                       |
| begin mrbayes;                                                        |
|     < YOUR COMMANDS HERE >;                                           |
| end;                                                                  |
| ```                                                                   |
+-----------------------------------------------------------------------+

Note that there are semicolons at the end of each command!

Even though the mrbayes block can simply be added below the data matrix
in the nexus file, we recommond keeping the data and the commands
separate. This way you can easily use the same data set with different
settings or programs. Write the following batch file and call it
algaemb\_batch.nex:

+-----------------------------------------------------------------------+
| **algaemb\_batch.nex:**                                               |
| ``` {style="font-size: 1.25em"}                                       |
| #NEXUS                                                                |
|                                                                       |
| [ Text in square brackets is interpreted as a comment and will not be |
|  read by the program ]                                                |
|                                                                       |
| begin mrbayes;                                                        |
|     set autoclose=yes nowarn=yes;                                     |
|                                                                       |
|     [ data file ]                                                     |
|     execute algaemb.nex;                                              |
|     outgroup Anacystis_nidulans;                                      |
|                                                                       |
|     [ substitution model ]                                            |
|     lset nst=2 rates=gamma ngammacat=4;                               |
|                                                                       |
|     [ priors ]                                                        |
|     prset brlenspr=unconstrained:exp(10.0) shapepr=exp(1.0) tratiopr= |
| beta(1.0,1.0) statefreqpr=dirichlet(1.0,1.0,1.0,1.0);                 |
|                                                                       |
|     [ mcmc settings ]                                                 |
|     mcmcp ngen=100000 samplefreq=100 printfreq=100 nruns=2 nchains=2  |
| stoprule=yes stopval=0.01;                                            |
|     mcmc;                                                             |
|                                                                       |
|     sump burninfrac=0.25;                                             |
|     sumt burninfrac=0.25;                                             |
|     quit;                                                             |
| end;                                                                  |
| ```                                                                   |
+-----------------------------------------------------------------------+

Now save the file, and - although we are not doing this now because we
do not want to overwrite our results - you could rerun the analysis by
providing MrBayes with the filename as a command line argument:
`mb32  algaemb_batch.nex`{style="font-size: 1.25em"}. In this case you
could also redirect the screen output to a file, or you can use the
**log** command in MrBayes. **Note:** alternatively you could also just
start MrBayes and execute **algaemb\_batch.nex** from the program's
command prompt.

### [ Summarizing and interpreting the results ]{#Summarizing_and_interpreting_the_results .mw-headline}

#### [ The sump command ]{#The_sump_command .mw-headline}

MrBayes saves information in several files. Only two types of these will
concern us today. One of them will be called **algaemb.nex.run1.p**.
This is the file in which the sampled parameter values from run 1 were
saved (there is also a corresponding file for run 2, both will be
summarized). This file is saved in tab-delimited format so that it is
easy to import into a spreadsheet program such as Excel. We will examine
this file graphically in a moment, but first let's get MrBayes to
summarize its contents for us.

At the MrBayes prompt, type the command sump. This will generate a crude
graph showing the log-likelihood as a function of time. Note that the
log-likelihood starts out low on the left (you started from a random
tree, remember), then quickly climbs to a constant value.

Below the graph, MrBayes provides the arithmetic mean and harmonic mean
of the marginal likelihood. The harmonic mean is used in estimating
Bayes factors, which are in turn useful for deciding which among
different models fits the data best on average. We will talk about how
to use this value in lecture, where you will also get some warnings
about Bayes factors calculated in this way.

The table at the end is quite useful. It shows the posterior mean,
median, variance and 95% credible interval for each parameter in your
model based on the samples taken during the run. The credible interval
shows the range of values of a parameter that account for the middle 95%
of its marginal posterior distribution. If the credible interval for
kappa is 3.8 to 6.8, then you can say that there is a 95% chance that
kappa is between 3.8 and 6.8 given your data (and of course the model).
The parameter TL represents the sum of all the branch lengths. Rather
than reported every branch length individually, MrBayes just keeps track
of their sum.

#### [ The sumt command ]{#The_sumt_command .mw-headline}

Now type the command sumt. This will summarize the trees that have been
saved in the files **algaemb.nex.run1.t** and **algaemb.nex.run2.t**.

The output of this command includes a bipartition (=split) table,
showing posterior probabilities for every split found in any tree
sampled during the run. After the bipartition table is shown a
majority-rule consensus tree containing all splits that had posterior
probability 0.5 or above.

MrBayes also calculates the maximum and average standard deviation of
split frequencies (should approach 0.0), as well as the [potential scale
reduction
factor](http://hosho.ees.hokudai.ac.jp/~kubo/Rdoc/library/coda/html/gelman.diag.html){.external
.text} (PSRF, should approach 1.0)^[\[5\]](#cite_note-gelman1992-4)^.
For my tree sample the output looked like this:

+-----------------------------------------------------------------------------------------+
| **MrBayes screen output:**                                                              |
| ``` {style="font-size: 1.25em"}                                                         |
|  Summary statistics for informative taxon bipartitions                                  |
|     (saved to file "algaemb.nex.tstat"):                                                |
|  ID   #obs    Probab.     Sd(s)+      Min(s)      Max(s)   Nruns                        |
|  ----------------------------------------------------------------                       |
|   9  1202    1.000000    0.000000    1.000000    1.000000    2                          |
|  10  1202    1.000000    0.000000    1.000000    1.000000    2                          |
|  11  1075    0.894343    0.017648    0.881864    0.906822    2                          |
|  12   887    0.737937    0.003530    0.735441    0.740433    2                          |
|  13   651    0.541597    0.003530    0.539101    0.544093    2                          |
|  14   478    0.397671    0.011766    0.389351    0.405990    2                          |
|  15   129    0.107321    0.008236    0.101498    0.113145    2                          |
|  16   122    0.101498    0.016472    0.089850    0.113145    2                          |
|  ----------------------------------------------------------------                       |
|  + Convergence diagnostic (standard deviation of split frequencies)                     |
|    should approach 0.0 as runs converge.                                                |
|  Summary statistics for branch and node parameters                                      |
|     (saved to file "algaemb.nex.vstat"):                                                |
|                                          95% HPD Interval                               |
|                                        --------------------                             |
|  Parameter      Mean       Variance     Lower       Upper       Median     PSRF+  Nruns |
|  -------------------------------------------------------------------------------------- |
|  length[1]     0.008367    0.000013    0.001950    0.015120    0.007852    1.001    2   |
|  length[2]     0.022923    0.000033    0.012460    0.034131    0.022379    1.002    2   |
|  length[3]     0.007468    0.000012    0.001151    0.014112    0.006961    0.999    2   |
|  length[4]     0.100903    0.000248    0.070782    0.132716    0.098969    1.000    2   |
|  length[5]     0.027781    0.000096    0.010363    0.047241    0.027005    0.999    2   |
|  length[6]     0.132494    0.000459    0.090394    0.172768    0.130331    1.002    2   |
|  length[7]     0.115070    0.000380    0.078286    0.152808    0.113921    0.999    2   |
|  length[8]     0.109665    0.000377    0.076268    0.152571    0.108245    1.005    2   |
|  length[9]     0.020557    0.000031    0.010935    0.031613    0.019942    0.999    2   |
|  length[10]    0.031238    0.000077    0.015405    0.048266    0.030336    1.002    2   |
|  length[11]    0.033435    0.000176    0.009834    0.060309    0.032323    0.999    2   |
|  length[12]    0.014773    0.000062    0.000372    0.029653    0.014318    1.001    2   |
|  length[13]    0.021518    0.000096    0.004489    0.041987    0.020622    0.999    2   |
|  length[14]    0.017349    0.000068    0.003676    0.033102    0.016950    0.998    2   |
|  length[15]    0.006425    0.000026    0.000008    0.014339    0.005335    1.029    2   |
|  length[16]    0.028166    0.000208    0.004058    0.052153    0.026935    1.029    2   |
|  -------------------------------------------------------------------------------------- |
|  + Convergence diagnostic (PSRF = Potential Scale Reduction Factor; Gelman              |
|    and Rubin, 1992) should approach 1.0 as runs converge. NA is reported when           |
|    deviation of parameter values within all runs is 0 or when a parameter               |
|    value (a branch length, for instance) is not sampled in all runs.                    |
|  Summary statistics for partitions with frequency >= 0.10 in at least one run:          |
|      Average standard deviation of split frequencies = 0.007648                         |
|      Maximum standard deviation of split frequencies = 0.017648                         |
|      Average PSRF for parameter values ( excluding NA and >10.0 ) = 1.004               |
|      Maximum PSRF for parameter values = 1.029                                          |
| ```                                                                                     |
+-----------------------------------------------------------------------------------------+

If you chose to save branch lengths (and we did), MrBayes shows a second
tree in which each branch is displayed in such a way that branch lengths
are proportional to their posterior mean. MrBayes keeps a running sum of
the branch lengths for particular splits it finds in trees as it reads
the file algaemb.nex.t. Before displaying this tree, it divides the sum
for each split by the total number of times it encountered the split to
get a simple average branch length for each split. It then draws the
tree so that branch lengths are proportional to these mean branch
lengths.

Finally, the last thing the sumt command does is tell you how many tree
topologies are in credible sets of various sizes. For example, in my
run, it said that the 99% credible set contained 18 trees. What does
this tell us? MrBayes orders tree topologies from most frequent to least
frequent (where frequency refers to the number of times they appear in
algaemb.nex.t). To construct the 99% credible set of trees, it begins by
adding the most frequent tree to the set. If that tree accounts for 99%
or more of the posterior probability (i.e. at least 99% of all the trees
in the algaemb.nex.t file have this topology), then MrBayes would say
that the 99% credible set contains 1 tree. If the most frequent tree
topology was not that frequent, then MrBayes would add the next most
frequent tree topology to the set. If the combined posterior probability
of both trees was at least 0.99, it would say that the 99% credible set
contains 2 trees. In our case, it had to add the top 18 trees to get the
total posterior probability up to 99%.

Type

```
quit
```

(or just `q`{style="font-size: 1.25em"}), to quit MrBayes now.

[ Other output files produced by MrBayes ]{#Other_output_files_produced_by_MrBayes .mw-headline}
------------------------------------------------------------------------------------------------

That's it for the lab today. You can look at plots of the other
parameters if you like. You should also spend some time opening the
other output files MrBayes produces in a text editor to make sure you
understand what information is saved in these files. Note that some of
MrBayes' output files are actually NEXUS tree files, which you can open
in FigTree. For example, **algaemb.nex.con.tre** contains the consensus
tree from the Bayesian analysis. The file **algaemb.nex.trprobs**
contains all distinct tree topologies, sorted from highest to lowest
posterior probability. The file **algaemb.nex.mcmc** contains useful
statistics about the MCMC run (e.g. proposal acceptance rates, etc.).

[ Using other programs to summarize MCMC results ]{#Using_other_programs_to_summarize_MCMC_results .mw-headline}
----------------------------------------------------------------------------------------------------------------

### [ Tracer ]{#Tracer .mw-headline}

The Java program Tracer is very useful for summarizing the results of
Bayesian phylogenetic analyses. Tracer was written to accompany the
program Beast, but it works well with the output file produced by
MrBayes as well.

After starting Tracer, choose File &gt; Import... to choose a parameter
sample file to display. Select the **algaemb.nex.run1.p** in your
working folder, then click the Open button to read it.

You should now see 8 rows of values in the table labeled Traces on the
left side of the main window. The first row (LnL) is selected by
default, and Tracer shows a histogram of log-likelihood values on the
right, with summary statistics above the histogram.

A histogram is perhaps not the most useful plot to make with the LnL
values. Click the Trace tab to see a trace plot (plot of the
log-likelihood through time).

Tracer determines the burn-in period using an undocumented algorithm.
You may wish to be more conservative than Tracer. Opinions vary about
burn-in. Some Bayesians feel it is important to exclude the first few
samples because it is obvious that the chains have not reached
stationarity at this point. Other Bayesians feel that if you are worried
about the effect of the earliest samples, then you definitely have not
run your chains long enough! You might be interested in reading [Charlie
Geyer's rant on
burn-in](http://www.stat.umn.edu/~charlie/mcmc/burn.html){.external
.text} some time.

Click the Estimates tab again at the top, then click the row labeled
kappa on the left.

+-----------------------------------------------------------------------+
| -   What is the posterior mean of kappa?                              |
| -   What is the 95% credible interval for kappa?                      |
+-----------------------------------------------------------------------+

Click the row labeled alpha on the left. This is the shape parameter of
the gamma distribution governing rates across sites.

+-----------------------------------------------------------------------+
| -   What is the posterior mean of alpha?                              |
| -   What is the 95% credible interval for alpha?                      |
| -   Is there rate heterogeneity among sites, or are all sites         |
|     evolving at nearly the same rate?                                 |
+-----------------------------------------------------------------------+

Click on the row labeled TL on the left (the Tree Length).

+-----------------------------------------------------------------------+
| -   What is the posterior mean tree length?                           |
| -   What is the mean edge length? (Hint: divide the tree length by    |
|     the number of edges, which is 2n-3 if n is the number of taxa.)   |
+-----------------------------------------------------------------------+

### [ AWTY ]{#AWTY .mw-headline}

[AWTY](http://king2.scs.fsu.edu/CEBProjects/awty/awty_start.php){.external
.text}^[\[6\]](#cite_note-awtyweb-5)[\[7\]](#cite_note-awtypub-6)^

[ Running MrBayes with no data ]{#Running_MrBayes_with_no_data .mw-headline}
----------------------------------------------------------------------------

Why would you want to run MrBayes with no data? Here's a possible
reason. You discover by reading the text that results from typing **help
prset** that MrBayes assumes, by default, the following branch length
prior: exp(10). What does the 10 mean here? Is this an exponential
distribution with mean 10 or is 10 the so-called "rate" parameter (a
common way to parameterize the exponential distribution)? If 10 is
correctly interpreted as the rate parameter, then the mean of the
distribution is 1/rate, or 0.1. Even good documentation such as that
provided for MrBayes does not explicitly spell out everything you might
want to know, but running MrBayes without data can provide answers, at
least to questions concerning prior distributions.

Also, it is not possible to place prior distributions directly on some
quantities of interest. For example, while you can specify a flat prior
on topologies, it is not possible to place a prior on a particular split
you are interested in. This is because the prior distribution of splits
is induced by the prior you place on topologies. Running a Bayesian MCMC
program without data is a good way to make sure you know what priors you
are actually placing on the quantities of interest. Even if you think
you know, running without data provides a good sanity check.

If there is no information in the data, the posterior distribution
equals the prior distribution. An MCMC analysis in such cases provides
an approximation of the prior.

To do this in version 3.2 you need to make a simple modification to the
batch file **algeamb\_batch.nex** above. Change the line\
`mcmcp ngen=100000 samplefreq=100 printfreq=100 nruns=2 nchains=2 stoprule=yes stopval=0.01;`{style="font-size: 1.25em"}\
to\
`mcmcp ngen=100000 samplefreq=100 printfreq=100 nruns=2 nchains=2 stoprule=yes stopval=0.01 data=no;`{style="font-size: 1.25em"}\

For version 3.1.2 execute the file **blank.nex** (see below) in MrBayes
(**NOTE: do not use this file with version 3.2. For some reason the
program becomes unresponsive when you try to do it.**). Here is what
this file looks like (use your favorite text editor to create this file
in the MrBayes directory):

+-----------------------------------------------------------------------+
| **blank.nex**                                                         |
| ``` {style="font-size: 1.25em"}                                       |
| #NEXUS                                                                |
| begin data;                                                           |
| dimensions ntax=4 nchar=1;                                            |
| format datatype=dna missing=? gap=-;                                  |
| matrix                                                                |
|   A ?                                                                 |
|   B ?                                                                 |
|   C ?                                                                 |
|   D ?                                                                 |
|   ;                                                                   |
| end;                                                                  |
|                                                                       |
| begin mrbayes;                                                        |
|   set autoclose=yes;                                                  |
|   prset brlenspr=unconstrained:exp(10.0);                             |
|   prset tratiopr=beta(1.0,1.0);                                       |
|   prset statefreqpr=Dirichlet(1.0,1.0,1.0,1.0);                       |
|   prset shapepr=exp(1.0);                                             |
|   lset nst=2 rates=gamma ngammacat=4;                                 |
|   mcmcp ngen=1000000 samplefreq=100 printfreq=100 nruns=1 nchains=1;  |
|   mcmc;                                                               |
| end;                                                                  |
| ```                                                                   |
+-----------------------------------------------------------------------+

Note that the data matrix consists of just one character, and that
character declares that data are missing for all taxa!

Type

```
mcmc
```

to perform the analysis. Because calculation of the likelihood is the
most time-consuming part of a Bayesian analysis, this analysis will go
quickly because the likelihood for just one site takes almost no time to
compute.

Consulting Bayes' formula, what value of the likelihood would cause the
posterior to equal the prior? Is this the value that MrBayes reports for
the log-likelihood in this case?

### [ Checking the shape parameter prior ]{#Checking_the_shape_parameter_prior .mw-headline}

Import the output file blank.nex.p in Tracer. Look first at the
histogram of alpha, the shape parameter of the gamma distribution.

What is the mean you expected for alpha based on the prset
shapepr=exp(1.0) command in the blank.nex file? What is the posterior
mean actually estimated by MrBayes (and presented by Tracer)? An
exponential distribution always starts high and approaches zero as you
move to the right along the x-axis. The highest point of the exponential
density function is 1/mean. If you look at the approximated density plot
(click on the Marginal Density tab), does it appear to approach 1/mean
at the value alpha=0.0?

### [ Checking the branch length prior ]{#Checking_the_branch_length_prior .mw-headline}

Now look at the histogram of TL, the tree length.

What is the posterior mean of TL, as reported by Tracer? What value did
you expect based on the prset brlenspr=unconstrained:exp(10) command?
Does the approximated posterior distribution of TL appear to be an
exponential distribution? The second and third questions are a bit
tricky, so I'll just give you the explanation. Please make sure this
explanation makes sense to you, however, and ask us to explain further
if it doesn't make sense. We told MrBayes to place an exponential prior
with mean 0.1 on each branch. There are 5 branches in a 4-taxon,
unrooted tree. Thus, 5 times 0.1 equals 0.5, which should be close to
the posterior mean you obtained for TL. That part is fairly
straightforward.

The marginal distribution of TL does not look at all like an exponential
distribution, despite the fact that TL should be the sum of 5
exponential distributions. It turns out that the sum of n independent
Exponential($\lambda$) distributions is a Gamma(n, 1 / $\lambda$) distribution. In our
case the tree length distribution is a sum of 5 independent
Exponential(10) distributions, which equals a Gamma(5, 0.1)
distribution. Such a Gamma distribution would have a mean of 0.5 and a
peak (mode) at 0.4. If you want to visualize this, fire up R and type
the following commands:

```
x <- seq(0, 2, .001)
y <- dgamma(x, shape=5, scale=0.1)
plot(x, y, type="l")
```

How does the Gamma(5, 0.1) density compare to the distribution of TL as
shown by Tracer? (Be sure to click the "Marginal Density" tab in Tracer)
