--a
select distinct on (НАЗВАНИЕ) НАЗВАНИЕ, ЛЬГОТА from СУДНО;

--b
select distinct ПОРТ_ПРИПИСКИ from СУДНО;

--c
select distinct ПОРТ from МЕСТА_ПОГРУЗКИ;