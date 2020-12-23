--a
select 
	НАЗВАНИЕ
from
	(select 
		НАЗВАНИЕ,
		max(СТОИМОСТЬ) as САМАЯ_ДОРОГАЯ
	from
		ПОГРУЗКА 
		inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ from СУДНО) as с
			on СУДНО = ИДЕНТИФИКАТОР
	where ДАТА in ('Понедельник', 'Вторник') 
	group by НАЗВАНИЕ) as foo
where САМАЯ_ДОРОГАЯ <= 100000;

--b
select 
	ДАТА,
	count(*)
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
		on МЕСТА_ПОГРУЗКИ = ИДЕНТИФИКАТОР
where ПОРТ = 'Владивосток'
group by ДАТА;

--c
select 
	НАЗВАНИЕ,
	ПРИЧАЛ,
	sum(СТОИМОСТЬ)
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, ПРИЧАЛ, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
		on МЕСТА_ПОГРУЗКИ = ИДЕНТИФИКАТОР
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ, ПОРТ_СКЛАДИРОВАНИЯ from ГРУЗ) as г
		on ГРУЗ = г.ИДЕНТИФИКАТОР
where ПОРТ = ПОРТ_СКЛАДИРОВАНИЯ
group by НАЗВАНИЕ, ПРИЧАЛ;

--d
select 
	НАЗВАНИЕ,
	count(distinct СУДНО)
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ, СТОИМОСТЬ from ГРУЗ) as г
		on ГРУЗ = ИДЕНТИФИКАТОР
where ДАТА > 'Понедельник'
group by НАЗВАНИЕ;
