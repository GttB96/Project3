/*  
Steps:
1)  run the show data_directory to get path name
2)  copy all_historical_csv and Current_Alt_Fuel_location.csv files into resulting path
3)  Change path in Copy statements below if different 
4)  run the copy statements and data should be imported
5)  run the select statements to verify that data imported

alternative would be to grant postgres permissions to current file locations and change the path to match in the copy statements - not recommended
*/
begin;

-- 1)
show data_directory;
-- 2)  copy files into directory listed 

-- 3)  change path in copy statements if necessary
-- 4)  run copy statements
-- note:  copy statement will error if already imported - you can recreate the table and try again if needed
COPY all_historical FROM 'C:/Program Files/PostgreSQL/14/data/all_historical.csv' DELIMITER ',' CSV HEADER;
COPY stations FROM 'C:/Program Files/PostgreSQL/14/data/Current_Alt_Fuel_location.csv' DELIMITER ',' CSV HEADER;

-- 5)  run selects to verify import worked.
select * from all_historical;
-- select count(1) from all_historical;

select * from stations;
-- select count(1) from stations;

commit;





