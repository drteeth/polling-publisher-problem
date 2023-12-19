# Sample project showing the peril of polling for rows in a table with concurrent writes.

If you are trying to implement a [Polling publisher](https://microservices.io/patterns/data/polling-publisher.html), and you are trying to save your progress via a high water mark, with concurrent writers, you can run into the problem in this example:

The example starts a write, starts a second concurrent write which finishes before the first, and then finally finishes the first. Reading concurrently between writes.

```shell
$ ./run

   id   |   tx_id   |   data
--------+-----------+--------
 51     |     816   |   bbb

 ```
 The first write has started but not finished, while the second write has finished.
 We might be tempted to use 51 has our high water mark, but....

```shell
   id   |   tx_id   |   data
--------+-----------+--------
 50     |     815   |   aaa
 51     |     816   |   bbb
```

After the first write completes, we see now a row with an earlier id has transaction ID has been added. If we had used 51 as our high water mark, we would have missed row 51.

### Running:

Create start the database and create the python virtual env
```shell
$ ./setup
```

Run the simulation. It will not always exhibit the problem behaviour. Try it a few times.
```shell
$ ./run
```
