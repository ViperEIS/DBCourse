--a
select 
	НАЗВАНИЕ,
	ПОРТ,
	ПРИЧАЛ
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ from СУДНО) as с
		on СУДНО = ИДЕНТИФИКАТОР
	inner join (select ИДЕНТИФИКАТОР, ПРИЧАЛ, ПОРТ, ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ from МЕСТА_ПОГРУЗКИ) as м
		on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
where м.ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ > 3
order by ПОРТ;

--b
select 
	НАЗВАНИЕ,
	ПОРТ_ПРИПИСКИ,
	ПОРТ
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ, ПОРТ_ПРИПИСКИ from СУДНО) as с
		on СУДНО = ИДЕНТИФИКАТОР
	inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
		on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
where СТОИМОСТЬ > 50000;

--c
select 
	г.НАЗВАНИЕ,
	г.СТОИМОСТЬ
from
	ПОГРУЗКА 
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ from СУДНО) as с
		on СУДНО = ИДЕНТИФИКАТОР
	inner join (select ИДЕНТИФИКАТОР, ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ from МЕСТА_ПОГРУЗКИ) as м
		on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
	inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ, СТОИМОСТЬ from ГРУЗ) as г
		on ГРУЗ = г.ИДЕНТИФИКАТОР
where с.НАЗВАНИЕ = 'Генуя' and м.ОТЧИСЛЕНИЯ_НА_ПОГРУЗКУ > 2;

--d
select
	НАЗВАНИЕ
from
	(select
		НАЗВАНИЕ,
		count(distinct ПОРТ)
	from
		ПОГРУЗКА 
		inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ from СУДНО) as с
			on СУДНО = ИДЕНТИФИКАТОР
		inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
			on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
	group by НАЗВАНИЕ
	having count(distinct ПОРТ) > 1) as foo
