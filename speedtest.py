from tkinter import ttk
import speedtest
import tkinter as tk
import threading

from assets import scripts
################################################################################################################################################################################
class SpeedTestGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.title("Steel Systems Speedtest")
        self.tk.call('source', 'assets/theme/sun-valley.tcl')
        self.tk.call('set_theme', 'dark')
        self.style = scripts.Style(self)
        self.titlebar = scripts.Titlebar(self)
        self.titlebar.pack(side="top", fill="x")
        self.configure()
################################################################################################################################################################################
        self.windowTitle = ttk.Label(self, text="SPEEDTEST", style="TLabel", font=("Bahnschrift", 24, "bold")).place(relx=.5, rely=.2, anchor="center")

        self.activateSpeedTest = ttk.Button(self, text="Begin", command=self.preSpeedTest, style="Accent.TButton").place(relx=.5, rely=.9, anchor="center", width=140)
 
        self.progressBar = ttk.Progressbar(self, value=50, orient=tk.HORIZONTAL, mode="indeterminate")
        self.progressBar.place(relx=.5, rely=.8, anchor="center", width=350)

        image = tk.PhotoImage(file ="assets/images/progress_circle_full_rest.png")
        image = image.subsample(25, 25)
        self.restCircle = ttk.Label(self)
        self.restCircle.place(relx=.5,rely=.8, anchor="center")
        self.restCircle.configure(image=image)
        self.restCircle.image=image
################################################################################################################################################################################
        self.downloadLabel = ttk.Label(self, text="Download Speed:", style="TLabel", font=("Bahnschrift", 10, "bold")).place(relx=.5, rely=.35, anchor="center")

        self.downloadBar = ttk.Progressbar(self, orient=tk.HORIZONTAL, mode="determinate")
        self.downloadBar.place(relx=.5, rely=.385, anchor="center", width=300)

        self.downloadAmount = ttk.Label(self, text="0.00 Mbps", style="TLabel", font=("Bahnschrift", 10, "bold"))
        self.downloadAmount.place(relx=.5, rely=.42, anchor="center")
################################################################################################################################################################################
        self.uploadLabel = ttk.Label(self, text="Upload Speed:", style="TLabel", font=("Bahnschrift", 10, "bold")).place(relx=.5, rely=.52, anchor="center")

        self.uploadBar = ttk.Progressbar(self, orient=tk.HORIZONTAL, mode="determinate")
        self.uploadBar.place(relx=.5, rely=.555, anchor="center", width=300)

        self.uploadAmount = ttk.Label(self, text="0.00 Mbps", style="TLabel", font=("Bahnschrift", 10, "bold"))
        self.uploadAmount.place(relx=.5, rely=.59, anchor="center")
################################################################################################################################################################################
        self.pingAmount = ttk.Label(self, text="Ping: 0 ms", style="TLabel", font=("Bahnschrift", 14, "bold"))
        self.pingAmount.place(relx=.5, rely=.68, anchor="center")
################################################################################################################################################################################
    def preSpeedTest(self):
        self.configureDefault()
        self.progressCircle = scripts.ProgressCircle(self, width=30, height=30, style="TLabel")
        self.progressCircle.place(relx=.5,rely=.8, anchor="center")
        self.progressCircle.play(interval=2)
        threading.Thread(target=lambda: self.progressBar.start(1)).start()
        threading.Thread(target=self.performSpeedTest).start()

    def performSpeedTest(self):
        downloadSpeed = "{:.2f}".format(initiateSpeedTest.download()/1000000)
        self.configureDownload(downloadSpeed)
        uploadSpeed = "{:.2f}".format(initiateSpeedTest.upload()/1000000)
        self.configureUpload(uploadSpeed)
        ping = int(initiateSpeedTest.results.ping)
        self.configurePing(ping)
        self.postSpeedTest()
    
    def postSpeedTest(self):
        self.progressCircle.stop()
        self.progressBar.stop()
        self.progressCircle.place_forget()
        self.progressBar.configure(mode="determinate", value=100)
        self.configureImage()

    def configureDefault(self):
        self.downloadBar.configure(value=0)
        self.downloadAmount.configure(text="0.00 Mbps")
        self.uploadBar.configure(value=0)
        self.uploadAmount.configure(text="0.00 Mbps")
        self.pingAmount.configure(text="Ping: 0 ms")
        self.progressBar.configure(value=50, mode="indeterminate")

    def configureDownload(self, download):
        self.downloadBar['maximum'] = 150
        self.downloadBar['value'] = download
        self.downloadAmount.configure(text=f"{str(download)} Mbps")
    
    def configureUpload(self, upload):
        self.uploadBar['maximum'] = 150
        self.uploadBar['value'] = upload
        self.uploadAmount.configure(text=f"{str(upload)} Mbps")
    
    def configurePing(self, ping):
        self.pingAmount.configure(text=f"Ping: {str(ping)} ms")

    def configureImage(self):
        image = tk.PhotoImage(file =f"assets/images/progress_circle_full_{self.getTheme()}.png")
        image = image.subsample(25, 25)
        self.restCircle.configure(image=image)
        self.restCircle.image=image
################################################################################################################################################################################
    def getTheme(self):
        return str(self.tk.call("ttk::style", "theme", "use")).split("-")[-1]

    def closeApplication(self):
        exit()
################################################################################################################################################################################
initiateSpeedTest = speedtest.Speedtest()
app = SpeedTestGUI()
app.mainloop()
