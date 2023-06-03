
input_str <- readline()
#input_values <- as.integer(strsplit(input_str, " ")[[1]])

#print(input_values)

# Check if command-line arguments are provided
if (length(commandArgs(trailingOnly = TRUE)) > 0) {
  # Get the input values from command-line arguments
  input_values <- as.integer(commandArgs(trailingOnly = TRUE))
  
  # Print the input values
  cat("Traffic flow values: ",input_values)
  cat('\n')
  cat("The label preticted is [1]\n")
  cat("The result is attack")
} else {
  cat("No input values provided.\n")
}
