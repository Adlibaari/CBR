import streamlit as st
import warnings
import numpy as np
warnings.filterwarnings("ignore")
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import re

url = "https://raw.githubusercontent.com/Adlibaari/CBR/main/bookdata.csv"
df = pd.read_csv(url)

# def recommend(bookTitle):
#     bookTitle=str(bookTitle)
    
#     if bookTitle in df["Book-Title"].values:
#         rating_count=pd.DataFrame(df["Book-Title"].value_counts())
#         rare_books=rating_count[rating_count["count"]<=200].index
#         common_books=df[~df["Book-Title"].isin(rare_books)]

#         if bookTitle in rare_books:
#             most_common=pd.Series(common_books["Book-Title"].unique()).sample(3).values
#             st.write("We can't give  you recommendations for this book \n ")
#             st.write("But you can try: \n ")
#             st.write("{}".format(most_common[0]), "\n")
#             st.write("{}".format(most_common[1]), "\n")
#             st.write("{}".format(most_common[2]), "\n")
#         else:
#             common_books=common_books.drop_duplicates(subset=["Book-Title"])
#             common_books.reset_index(inplace=True)
#             common_books["index"]=[i for i in range(common_books.shape[0])]
#             targets=["Book-Title","Book-Author","Publisher"]
#             common_books["all_features"] = [" ".join(common_books[targets].iloc[i,].values) for i in range(common_books[targets].shape[0])]
#             vectorizer=CountVectorizer()
#             common_booksVector=vectorizer.fit_transform(common_books["all_features"])
#             similarity=cosine_similarity(common_booksVector)
#             index=common_books[common_books["Book-Title"]==bookTitle]["index"].values[0]
#             similar_books=list(enumerate(similarity[index]))
#             similar_booksSorted=sorted(similar_books,key=lambda x:x[1],reverse=True)[1:6]
#             books=[]
#             for i in range(len(similar_booksSorted)):
                
#                 books.append(common_books[common_books["index"]==similar_booksSorted[i][0]]["Book-Title"].item())
                
#             for i in range(len(books)):
#                 st.write(books[i], "\n")

#     else:
#         st.write("COULD NOT FIND THE BOOK YOU CHOSEN")

url2 = "https://raw.githubusercontent.com/Adlibaari/CBR/main/book_list.csv"
booklist = pd.read_csv(url2)

# book = st.text_input("Book you want recommendation based off of")

def users_choice():
    users_fav=new_df[new_df["User-ID"]==id].sort_values(["Book-Rating"],ascending=False)[0:5]
    users_fav=pd.DataFrame(userInput)
    return users_fav

def user_based(new_df,id):
    if id not in new_df["User-ID"].values:
        print("❌ User NOT FOUND ❌")
        
        
    else:
        index=np.where(users_pivot.index==id)[0][0]
        similarity=cosine_similarity(users_pivot)
        similar_users=list(enumerate(similarity[index]))
        similar_users = sorted(similar_users,key = lambda x:x[1],reverse=True)[0:5]
    
        user_rec=[]
    
        for i in similar_users:
                data=df[df["User-ID"]==users_pivot.index[i[0]]]
                user_rec.extend(list(data.drop_duplicates("User-ID")["User-ID"].values))
        
    return user_rec

def common(new_df,user,user_id):
    x=new_df[new_df["User-ID"]==user_id]
    recommend_books=[]
    user=list(user)
    for i in user:
        y=new_df[(new_df["User-ID"]==i)]
        books=y.loc[~y["Book-Title"].isin(x["Book-Title"]),:]
        books=books.sort_values(["Book-Rating"],ascending=False)[0:5]
        recommend_books.extend(books["Book-Title"].values)
        
    return recommend_books[0:5]

st.title(' :book: Book Recommendation :book:')

with st.form("my form"):
    Book1 = st.selectbox("Judul Buku 1:",booklist,index=None)
    Book2 = st.selectbox("Judul Buku 2:",booklist,index=None)
    Book3 = st.selectbox("Judul Buku 3:",booklist,index=None)
    Book4 = st.selectbox("Judul Buku 4:",booklist,index=None)
    Book5 = st.selectbox("Judul Buku 5:",booklist,index=None)

    submitted = st.form_submit_button("Submit")
    if submitted: 
        st.divider()
        st.header('You Might Like')
        
        new_df=df[df['User-ID'].map(df['User-ID'].value_counts()) > 200]  # Drop users who vote less than 200 times.
        
        userInput = [{"Book-Title": Book1,"User-ID":278859, "Book-Rating": 10},
                     {"Book-Title": Book2, "User-ID":278859, "Book-Rating": 10},
                     {"Book-Title": Book3, "User-ID":278859, "Book-Rating": 10},
                     {"Book-Title": Book4, "User-ID":278859, "Book-Rating": 10},
                     {"Book-Title": Book5, "User-ID":278859, "Book-Rating": 10}]
            #users_fav=new_df[new_df["User-ID"]==id].sort_values(["Book-Rating"],ascending=False)[0:5]
        users_fav=pd.DataFrame(userInput)
        
        new_df = pd.concat([new_df, users_fav], ignore_index=True)
        
        users_pivot=new_df.pivot_table(index=["User-ID"],columns=["Book-Title"],values="Book-Rating")
        users_pivot.fillna(0,inplace=True)
       
        user_id=278859
        user_choice_df=pd.DataFrame(users_choice())
        user_favorite=users_choice()
        n=len(user_choice_df["Book-Title"].values)
             
        # for i in range(n):
        #         st.write(user_choice_df["Book-Title"].values[i], "\n")
        
        user_based_rec=user_based(new_df,user_id)
        books_for_user=common(new_df,user_based_rec,user_id)
        books_for_userDF=pd.DataFrame(books_for_user,columns=["Book-Title"])

        captions = []
        images = []
        for i in range(5):
            captions.append(books_for_user[i])
            images.append(new_df.loc[new_df["Book-Title"]==books_for_userDF["Book-Title"].tolist()[i],"Image-URL-L"][:1].values[0])

        st.image(images, width = 250, caption = captions)
# if book:
#     recommend(book)
