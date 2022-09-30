CREATE FUNCTION execution_tree 
(
	@parentID TEXT
)
RETURNS TABLE 
AS RETURN (
    	WITH tree_view AS (
		SELECT ID,
			 Parent_ID,
			 Name,
			 Label,
			 0 AS level,
			 CAST(ID AS varchar(50)) AS order_sequence
		FROM ExecutionOrder_test
		WHERE Parent_ID=@parentID
     
	UNION ALL
 
		SELECT parent.ID,
			 parent.Parent_ID,
			 parent.Name,
			 parent.Label,
			 level + 1 AS level,
			 CAST(CONCAT(order_sequence, '_', CAST(parent.ID AS VARCHAR (50))) AS VARCHAR(50)) AS order_sequence
		FROM ExecutionOrder_test parent
		JOIN tree_view tv
		  ON parent.Parent_ID = tv.ID
	)
    
	SELECT
	   CONCAT(LEFT('---------------------------------------------',level*3), Name) AS ExecutionOrder_test_tree, 
	   Label
	FROM tree_view
)

	--ORDER BY order_sequence;

--SELECT * FROM execution_tree('15104725');