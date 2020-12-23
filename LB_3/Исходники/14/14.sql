--a
select
	НАЗВАНИЕ
from 
	(select 
		НАЗВАНИЕ,
		ЛГ
	from
		(select 
			НАЗВАНИЕ,
			min(ЛЬГОТА) as ЛГ
		from
			ПОГРУЗКА 
			inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ, ЛЬГОТА from СУДНО) as с
				on СУДНО = ИДЕНТИФИКАТОР
			inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
				on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
		group by НАЗВАНИЕ
		having 
			count(distinct ПОРТ) = (select count(distinct ПОРТ) from МЕСТА_ПОГРУЗКИ)) as foo) as foo
where ЛГ < (select avg(ЛЬГОТА) from СУДНО);

--b
select
	count(ПРИЧАЛ)
from МЕСТА_ПОГРУЗКИ
group by ПОРТ
having ПОРТ = 'Владивосток';

--c
select 
	avg(СТОИМОСТЬ)
from 
	(select 
		СТОИМОСТЬ
	from
		ПОГРУЗКА 
		inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
			on МЕСТА_ПОГРУЗКИ = ИДЕНТИФИКАТОР
	where ПОРТ = 'Одесса') as foo;

--d
select 
	sum(СТОИМОСТЬ)
from 
	(select 
		СТОИМОСТЬ
	from
		ПОГРУЗКА 
		inner join (select ИДЕНТИФИКАТОР, ПОРТ_ПРИПИСКИ from СУДНО) as с
			on МЕСТА_ПОГРУЗКИ = ИДЕНТИФИКАТОР
		inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
			on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
	where ПОРТ_ПРИПИСКИ != ПОРТ) as foo;


