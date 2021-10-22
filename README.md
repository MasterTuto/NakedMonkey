<p align="center"> <img src="https://github.com/MasterTuto/NakedMonkey/blob/main/man-gd8b2938e5_1280.png?raw=true" width="120px"></p>
<p align="center"> <strong>NM - Roberto :moyai:</strong> </p>
<p align="center"> An interesting Telegram bot for CodeForces problem recommendation </p>
<hr/>

## Is it hosted somewhere?

No, you may either run it on your computer or host somewhere else. It also currently does not support Web Hooks, it ocasionally sends a query to Telegram API to get updates.

## How can I use it?

There is currently only 1 working command. But there are plans of adding two more. I will describe them below:

* First things first: Any of the commands below can be used with the same parameters, but the behavior may be different. The parameters are:  
  * `any word` well, any word is considered a tag. Tags with multiple words must be in parenthesis. E.g. dp implementation "binary search"
  * `n:` is the number of problemas to query, it must be greater than 0. E.g. n:10, n:5
  * `r:` is the rating, it may be a single value or a range. In case it is a range, it can have a starting value, an end value or both (including).
  E.g.: r:1000 (search for problems with rating exactly equal to 1000), r:800- (search for problems with rating at least 800), r:-2500
  (filters the problems with the maximum (including) of 250 of rating), r:1100-1800 (well, you may have got already).
  * `@` indicates users to filter i.e. does not show problems you already submitted. E.g. @tourist.

* `/rand`: Responds with random problem with given queryies, default config is n:1, which means it returns a single random problem.
* `/recommend`: * not yet implemented *, but supposedly will recommend problems based on your submissions.
* `/gen`: * not yet implemented * , but supposedly will generate a PDF file containig _n_ problems, of _W_ tags with _R_ ratings which _AT_ users haven't answered.

## How can I use it?

run `directapi.py`

## Can I see it working?

Of course, here is a screenshot:

<img src="https://github.com/MasterTuto/NakedMonkey/blob/main/imagem_2021-10-22_115113.png?raw=true" width="400" />

