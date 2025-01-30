import ollama
import customtkinter as ctk
import os
from PIL import ImageTk



client = ollama.Client()

class ChatApp:
    def __init__(self, root):
        self.root=root
        # openstack_icon = self.root.iconbitmap('logo.ico')
        self.iconpath = ImageTk.PhotoImage(file=os.path.join("R:/Github/chatBot/assets/logo.png"))
        self.root.wm_iconbitmap()
        self.root.iconphoto(False, self.iconpath)
        # self.root.wm_iconbitmap("\logo.ico")
        # self.root.after(201, lambda :root.iconbitmap('logo.ico'))
        self.root.title("DeepSeek cb_deepseek-r1:32B")
        self.root.geometry("1000x500,+800+250")
        self.root.configure(bg_color="#101010",fg_color="#101010")
        # self.root.resizable(0,0)
        self.root.columnconfigure(1,weight=1)
        self.root.rowconfigure(0,weight=1)
        # self.root.rowconfigure(1,weight=1)
        self.rowCounter=1
        self.buttonAvailabilityFlag=True

        # sidebarframe=ctk.CTkFrame(root,fg_color="#101010",border_color="#505050",border_width=1,width=200)
        # sidebarframe.grid(row=0,column=0,rowspan=2,sticky="nsew",padx=(10,5),pady=(10,10))
        # sidebarframe.columnconfigure(1,weight=1)

        # ctk.CTkLabel(sidebarframe, text="Model:", anchor="w").grid(row=0,column=0,sticky="w",padx=5,pady=5)
        # ctk.CTkOptionMenu(sidebarframe,dropdown_fg_color="#292929",dropdown_hover_color="#404040",fg_color="#292929",button_color="#404040",button_hover_color="#404040",values=["Sentinel"]).grid(row=0, column=2,sticky="e",padx=5,pady=5)

        # ctk.CTkLabel(sidebarframe, text="Creativity:", anchor="w").grid(row=1,column=0,sticky="w",padx=5,pady=5)
        # ctk.CTkOptionMenu(sidebarframe,dropdown_fg_color="#292929",dropdown_hover_color="#404040",fg_color="#292929",button_color="#404040",button_hover_color="#404040",values=["1","2","3","4","5","6","7"]).grid(row=1, column=2,sticky="e",padx=5,pady=5)

        self.chatframe=ctk.CTkScrollableFrame(root,fg_color="#202020",border_color="#505050",border_width=1)
        self.chatframe.grid(row=0,column=1,sticky="nsew",padx=(10,10),pady=(10,0))
        self.chatframe.columnconfigure(0,weight=1)
        self.chatframe.rowconfigure(0,weight=1)
        messageframe=ctk.CTkFrame(root,fg_color="#101010",border_width=0,height=50)
        messageframe.grid(row=1,column=1,sticky="nsew",padx=0,pady=0)
        messageframe.columnconfigure(0,weight=1)
        messageframe.rowconfigure(0,weight=1)
        self.constructor_chatContainer("MODEL","Hello there. \nHow can be of assistance today?").grid(row=self.rowCounter,column=0,sticky="nsew",padx=0,pady=0)
        # self.constructor_chatContainer("USER","").grid(row=self.rowCounter,column=0,sticky="nsew",padx=2,pady=2)
        # self.constructor_chatContainer("SYSTEM","SYSTEM ERROR! PLEASE TRY AGAIN.").grid(row=self.rowCounter,column=0,sticky="nsew",padx=2,pady=2)

        self.textEntry=ctk.CTkEntry(messageframe,border_color="#505050",border_width=1,placeholder_text="Prompt...",height=40)
        self.textEntry.grid(row=0,column=0,sticky="nsew",padx=(10,5),pady=(5,10))
        self.sendButton=ctk.CTkButton(messageframe,text="Send",hover_color="#101050",border_color="blue",border_width=1,bg_color="transparent",fg_color="#101010",command=lambda: self.getInput(str(self.textEntry.get())))
        self.sendButton.grid(row=0,column=1,sticky="nsew",padx=(0,10),pady=(5,10))
        self.textEntry.bind('<Return>', lambda event: self.getInput(str(self.textEntry.get()))) #:)


    def constructor_chatContainer(self,caller,myText):
        self.rowCounter+=1
        chatContainer=ctk.CTkFrame(self.chatframe,fg_color="#202020",border_width=0)
        chatContainer.columnconfigure(1,weight=1)
        chatCard=ctk.CTkFrame(chatContainer,fg_color="#101016",border_color="#505050",border_width=1,width=200)
        if caller=="MODEL":
            stickyPlace="nsw"
        elif caller=="USER":
            stickyPlace="nse"
        elif caller=="SYSTEM":
            stickyPlace="ns"
        else:
            self.constructor_chatContainer("SYSTEM","SYSTEM ERROR! PLEASE TRY AGAIN.").grid(row=self.rowCounter,column=0,sticky="nsew",padx=2,pady=2)
            print("Error: Caller not specified.")
            stickyPlace="ns"


        
        
        chatCard.grid(row=1,column=1,sticky=stickyPlace,padx=5,pady=5)
        chatCard.columnconfigure(0,weight=1)
        chatCard.rowconfigure(0,weight=1)
        
        thisText=ctk.CTkLabel(chatCard,text=myText,wraplength=300,justify="left")
        thisText.grid(row=0,column=0,sticky="nsew",padx=2,pady=2,ipadx=9,ipady=9)
        return chatContainer

    def getInput(self,message):
        self.textEntry.delete(0,ctk.END) # Nice
        if message=="":
            self.constructor_chatContainer("MODEL","?").grid(row=self.rowCounter,column=0,sticky="nsew",padx=2,pady=2)
            return
        # self.buttonAvailabilityFlag=False
        # self.sendButton.configure(state="disabled")
        self.constructor_chatContainer("USER",message).grid(row=self.rowCounter,column=0,sticky="nsew",padx=2,pady=2)
        self.getResponse(message)

    def getResponse(self,message):
        

        
        model = "deepseek-r1:8b"
        

        # Generate an initial response from the model
        response = client.generate(model=model, prompt=message)
        # print(f"Response from model: {model}")
        # print(response.response)
        thisResponse=str(response.response)
        while thisResponse==False:
            self.sendButton.configure(state="disabled")
        self.sendButton.configure(state="normal")
        self.constructor_chatContainer("MODEL",thisResponse).grid(row=self.rowCounter,column=0,sticky="nsew",padx=2,pady=2)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app_root=ctk.CTk()
    app=ChatApp(app_root)
    app_root.mainloop()