--a
select 
	ПРИЧАЛ
from
	МЕСТА_ПОГРУЗКИ м
where exists (
	select 1
	from МЕСТА_ПОГРУЗКИ
	where м.ПРИЧАЛ not in
		(select 
			ПРИЧАЛ
		from
			ПОГРУЗКА 
			inner join (select ИДЕНТИФИКАТОР, ПОРТ_ПРИПИСКИ from СУДНО) as с
				on СУДНО = ИДЕНТИФИКАТОР
			inner join (select ИДЕНТИФИКАТОР, ПРИЧАЛ from МЕСТА_ПОГРУЗКИ) as м
				on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
		where ПОРТ_ПРИПИСКИ not in ('Одесса', 'Мурманск') or ДАТА < 'Пятница')
	);
	
--b
select 
	НАЗВАНИЕ
from 
	СУДНО с
where exists (
	select 1
	from СУДНО
	where с.НАЗВАНИЕ in
		(select 
			НАЗВАНИЕ
		from 
			(select
				НАЗВАНИЕ,
				count(ПРИЧАЛ)
			from
				ПОГРУЗКА 
				inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ from СУДНО) as с
					on СУДНО = ИДЕНТИФИКАТОР
				inner join (select ИДЕНТИФИКАТОР, ПРИЧАЛ from МЕСТА_ПОГРУЗКИ) as м
					on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
			group by НАЗВАНИЕ having count(ПРИЧАЛ) = count(distinct ПРИЧАЛ)) as foo)
	);
	
--c
select 
	НАЗВАНИЕ
from
	ГРУЗ г
where exists (
	select 1
	from ГРУЗ
	where г.НАЗВАНИЕ not in
		(select 
			НАЗВАНИЕ
		from
			ПОГРУЗКА 
			inner join (select ИДЕНТИФИКАТОР, ПОРТ_ПРИПИСКИ from СУДНО) as с
				on СУДНО = ИДЕНТИФИКАТОР
			inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ, ПОРТ_СКЛАДИРОВАНИЯ from ГРУЗ) as г
				on ГРУЗ = г.ИДЕНТИФИКАТОР
		where ПОРТ_СКЛАДИРОВАНИЯ = ПОРТ_ПРИПИСКИ)
	);
	
--d
select 
	НАЗВАНИЕ
from
	ГРУЗ г
where exists (
	select 1
	from ГРУЗ
	where г.НАЗВАНИЕ in
		(select 
			НАЗВАНИЕ
		from
			ПОГРУЗКА 
			inner join (select ИДЕНТИФИКАТОР, ПОРТ_ПРИПИСКИ from СУДНО) as с
				on СУДНО = ИДЕНТИФИКАТОР
			inner join (select ИДЕНТИФИКАТОР, ПОРТ from МЕСТА_ПОГРУЗКИ) as м
				on МЕСТА_ПОГРУЗКИ = м.ИДЕНТИФИКАТОР
			inner join (select ИДЕНТИФИКАТОР, НАЗВАНИЕ from ГРУЗ) as г
				on ГРУЗ = г.ИДЕНТИФИКАТОР
		where 
			ПОРТ_ПРИПИСКИ = 'Владивосток' and 
			ПОРТ = 'Одесса' and 
			ДАТА between 'Вторник' and 'Четверг')
	);
