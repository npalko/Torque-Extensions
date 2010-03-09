

"""
DESIGN NOTES

Model Limitations
* Every table must have a Primary Key
    * which is definited by only one column, autoincrementing
* Unicode columns used for everything
* Don't support NUMERIC; only DECIMAL

Unique Constraints
* Specified as an index

Autoincrementing and Sequences
* Sequences are an implementation detail left up to the ORM. 


        
Tables organized as a collection of 
    column
    index
    foreign-key



Need to fix foreign key automatic name        

"""