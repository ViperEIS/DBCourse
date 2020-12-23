update ПОГРУЗКА
set СТОИМОСТЬ = СТОИМОСТЬ * ((100 - cast(СУДНО.ЛЬГОТА as decimal)) / 100) from СУДНО
where ПОГРУЗКА.СУДНО = СУДНО.ИДЕНТИФИКАТОР;
select * into tmp from ПОГРУЗКА order by НОМЕР_ВЕДОМОСТИ;
drop table ПОГРУЗКА;
select * into ПОГРУЗКА from tmp;
drop table tmp;
select СТОИМОСТЬ from ПОГРУЗКА;