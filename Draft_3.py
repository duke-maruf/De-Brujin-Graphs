from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class DNAAssemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Sequence Assembler")
        self.root.geometry("800x600")
        self.setup_ui()
        
    def setup_ui(self):
        bg_color, fg_color = "#e8f5e9", "#1b5e20"
        accent_color, button_color = "#43a047", "#a5d6a7"
        text_bg, text_fg = "#ffffff", "#000000"
        
        self.root.configure(bg=bg_color)
        style = ttk.Style()
        style.configure(".", background=bg_color, foreground=fg_color)
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TLabelframe", background=bg_color, foreground=accent_color)
        style.configure("TLabelframe.Label", background=bg_color, foreground=accent_color)
        style.configure("TButton", background=button_color, foreground=fg_color)
        style.map("TButton", background=[('active', accent_color), ('pressed', '#2e7d32')])
        
        text_options = {'bg': text_bg, 'fg': text_fg, 'insertbackground': text_fg, 
                       'selectbackground': accent_color, 'font': ("Courier", 10)}
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        input_frame = ttk.LabelFrame(main_frame, text="Input DNA Sequences", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, width=80, wrap=tk.WORD, **text_options)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        ttk.Label(input_frame, text="Enter DNA sequences").pack()
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Process", command=self.process_input).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        param_frame = ttk.LabelFrame(main_frame, text="Assembly Parameters", padding=10)
        param_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(param_frame, text="K-mer size:").grid(row=0, column=0, sticky=tk.W)
        self.k_entry = ttk.Entry(param_frame, width=5)
        self.k_entry.grid(row=0, column=1, sticky=tk.W)
        ttk.Button(param_frame, text="Assemble", command=self.assemble).grid(row=0, column=2, padx=10)
        
        result_frame = ttk.LabelFrame(main_frame, text="Assembly Results", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.result_notebook = ttk.Notebook(result_frame)
        self.result_notebook.pack(fill=tk.BOTH, expand=True)
        
        graph_tab = ttk.Frame(self.result_notebook)
        self.graph_text = scrolledtext.ScrolledText(graph_tab, height=10, width=80, wrap=tk.NONE, **text_options)
        self.graph_text.pack(fill=tk.BOTH, expand=True)
        self.result_notebook.add(graph_tab, text="De Bruijn Graph")
        
        path_tab = ttk.Frame(self.result_notebook)
        self.path_text = scrolledtext.ScrolledText(path_tab, height=5, width=80, wrap=tk.NONE, **text_options)
        self.path_text.pack(fill=tk.BOTH, expand=True)
        self.result_notebook.add(path_tab, text="Eulerian Path")
        
        seq_tab = ttk.Frame(self.result_notebook)
        self.seq_text = scrolledtext.ScrolledText(seq_tab, height=5, width=80, wrap=tk.NONE, **text_options)
        self.seq_text.pack(fill=tk.BOTH, expand=True)
        self.result_notebook.add(seq_tab, text="Assembled Sequence")
    
    def process_input(self):
        input_data = self.input_text.get("1.0", tk.END).strip().split('\n')
        self.sequences = [s.strip().upper() for s in input_data if s.strip()]
        invalid_seqs = [s for s in self.sequences if not all(c in "ACGT" for c in s)]
        self.sequences = [s for s in self.sequences if all(c in "ACGT" for c in s)]
        
        if invalid_seqs:
            messagebox.showwarning("Invalid Sequences", f"Invalid sequences:\n{', '.join(invalid_seqs)}\nIgnored.")
        if not self.sequences:
            messagebox.showerror("Error", "No valid DNA sequences!")
        else:
            messagebox.showinfo("Success", f"{len(self.sequences)} sequences loaded.")
    
    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self.graph_text.delete("1.0", tk.END)
        self.path_text.delete("1.0", tk.END)
        self.seq_text.delete("1.0", tk.END)
    
    def assemble(self):
        if not hasattr(self, 'sequences') or not self.sequences:
            messagebox.showerror("Error", "Input sequences first!")
            return
        
        try:
            k = int(self.k_entry.get())
            if k < 2: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "K must be integer ≥ 2")
            return
        
        km = [x[i:i+k] for x in self.sequences for i in range(len(x)-k+1)]
        g, ind, outd = defaultdict(list), defaultdict(int), defaultdict(int)
        
        for x in km:
            a, b = x[:-1], x[1:]
            g[a].append(b)
            outd[a] += 1
            ind[b] += 1
        
        st = next((n for n in g if outd[n] > ind[n]), next(iter(g)))
        stk, res = [st], []
        
        while stk:
            cur = stk[-1]
            if g[cur]:
                stk.append(g[cur].pop())
            else:
                res.append(stk.pop())
        
        p = res[::-1]
        s = p[0] + ''.join(n[-1] for n in p[1:])
        
        self.graph_text.delete("1.0", tk.END)
        self.graph_text.insert(tk.END, "De Bruijn Graph:\n\n" + '\n'.join(f"{a} -> {', '.join(b)}" for a, b in g.items()))
        self.path_text.delete("1.0", tk.END)
        self.path_text.insert(tk.END, "Eulerian Path:\n\n" + " -> ".join(p))
        self.seq_text.delete("1.0", tk.END)
        self.seq_text.insert(tk.END, "Assembled Sequence:\n\n" + s)

def main():
    root = tk.Tk()
    DNAAssemblerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()