# print("Enter the size of list")
n=int(input())
# print("Enter the elements of the list")
str=input()
# # Step 1: Split the string into a list of substrings
numbers_list_str = str.split()

# Step 2: Convert each substring to an integer
numbers_list = [int(num) for num in numbers_list_str]

# n=len(numbers_list)

#-----------------------------------------------------------------------------------------

# Solution 1: Recursion

# def optimal_score(list_of_numbers):
    
#     if len(list_of_numbers)==1:
#         return list_of_numbers[0]
    
#     return sum(list_of_numbers)-min(optimal_score(list_of_numbers[1:]),optimal_score(list_of_numbers[:-1]))

# if optimal_score(numbers_list) > sum(numbers_list)/2:
#     print("Player 1 Wins")
# elif optimal_score(numbers_list) < sum(numbers_list)/2:
#     print("Player 2 Wins")
# else:
#     print("Draw")

#-----------------------------------------------------------------------------------------

# Solution 2: Dynamic  Programing


n=len(numbers_list)
# print(sum(numbers_list))
prefix_sum_list = [0] * n 

prefix_sum_list[0]=numbers_list[0]
for i in range(1,n):
    prefix_sum_list[i]=prefix_sum_list[i-1]+numbers_list[i]

# print(prefix_sum_list)


answers_list = [[None for _ in range(n)] for _ in range(n)]      #initialise list



for i in range(n):
    answers_list[i][i]=numbers_list[i]

for i in range(1,n):
    for j in range(n-i):
        if (j+i<n):
            # print("-----------------")
            # print(numbers_list)
            # print(numbers_list[j:j+i+1])
            # print(prefix_sum_list)
            # print("i:",i)
            # print("j:",j)
            # print(prefix_sum_list[i+j])
            # print(prefix_sum_list[j])
            
            # print(sum(numbers_list[j:j+i+1]))
            # print(prefix_sum_list[i+j]-prefix_sum_list[j-1])
            # print("--------------------")
            # answers_list[j][j+i] = sum(numbers_list[j:j+i+1]) - min(answers_list[j+1][i+j],answers_list[j][j+i-1])
            if j>0:
                answers_list[j][j+i] = prefix_sum_list[i+j]-prefix_sum_list[j-1] - min(answers_list[j+1][i+j],answers_list[j][j+i-1])
            else:
                answers_list[j][j+i] = prefix_sum_list[i+j] - min(answers_list[j+1][i+j],answers_list[j][j+i-1])
       
                 
print(answers_list[0][n-1])    
            
# if answers_list[0][n-1]>sum(numbers_list)/2:
#     print("Player 1 wins")
# elif answers_list[0][n-1]<sum(numbers_list)/2:
#     print("Player 2 wins")     
# else:
#     print("Its a draw")
        
    






