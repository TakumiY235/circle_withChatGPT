import tkinter as tk
import time
import threading

# ウィンドウの初期化
window = tk.Tk()
window.title("Scaling Circle")
window.geometry("800x600")
window.configure(bg="black")  # ウィンドウの背景色を黒に設定

# キャンバスの作成
canvas = tk.Canvas(window, bg="black", highlightthickness=0)
canvas.pack(expand=True, fill="both")  # キャンバスをウィンドウ全体に拡大

# 円の初期設定
initial_radius = 100
enlarge_factor = 2.0
shrink_factor = 1.0
line_width = 5  # 円を描画する線の太さを設定

# キャンバスのサイズを円が完全に表示されるサイズに設定
canvas_width = initial_radius * 2 * enlarge_factor + 20
canvas_height = initial_radius * 2 * enlarge_factor + 20
canvas.config(width=canvas_width, height=canvas_height)


# ウィンドウのサイズ変更時にキャンバスを中央に配置
def center_canvas(event):
    canvas.update()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    canvas.place(x=(window.winfo_width() - canvas_width) / 2, y=(window.winfo_height() - canvas_height) / 2)


window.bind("<Configure>", center_canvas)

# アニメーションの時間設定（秒）
enlarge_time = 4
stop_time = 7
shrink_time = 8

# 秒数カウントラベルの初期化
labels = []
y_offsets = [-30, 0, 30, 60]  # テキストの垂直位置のオフセット

for label_text, y_offset in zip(["Total Seconds: 0", "Enlarge Seconds: 0", "Stop Seconds: 0", "Shrink Seconds: 0"],
                                y_offsets):
    label = canvas.create_text(canvas_width / 2, canvas_height / 2 + y_offset, text=label_text, fill="white",
                               anchor="center")
    labels.append((label, y_offset))

# 円を描画
circle = canvas.create_oval(
    canvas.winfo_reqwidth() / 2 - initial_radius,
    canvas.winfo_reqheight() / 2 - initial_radius,
    canvas.winfo_reqwidth() / 2 + initial_radius,
    canvas.winfo_reqheight() / 2 + initial_radius,
    outline="gray", width=line_width, tags="circle"
)

# アニメーションスレッドを開始
animation_running = True


def animate_circle():
    last_action_time = time.time()
    scale = 1.0  # 初期のスケールを設定

    # 秒数カウントを初期化
    elapsed_seconds = 0
    enlarge_seconds, stop_seconds, shrink_seconds = 0, 0, 0

    while True:
        if animation_running:
            current_time = time.time()
            elapsed_time = current_time - last_action_time
            elapsed_seconds = int(elapsed_time)

            if elapsed_time < enlarge_time:
                # 拡大中
                scale = 1.0 + (enlarge_factor - 1) * (elapsed_time / enlarge_time)
                enlarge_seconds = elapsed_seconds

            elif elapsed_time < enlarge_time + stop_time:
                # 停止中
                stop_seconds = elapsed_seconds - enlarge_seconds

            else:
                # 縮小中
                scale = enlarge_factor - (enlarge_factor - shrink_factor) * (
                        elapsed_time - (enlarge_time + stop_time)) / shrink_time
                shrink_seconds = elapsed_seconds - (enlarge_seconds + stop_seconds)

                if elapsed_time >= enlarge_time + stop_time + shrink_time:
                    # アニメーションサイクルをリセット
                    last_action_time = time.time()
                    enlarge_seconds, stop_seconds, shrink_seconds = 0, 0, 0
                    scale = 1.0  # 初期のスケールに戻す

            # 円を描画
            canvas.coords("circle",
                          canvas.winfo_reqwidth() / 2 - initial_radius * scale,
                          canvas.winfo_reqheight() / 2 - initial_radius * scale,
                          canvas.winfo_reqwidth() / 2 + initial_radius * scale,
                          canvas.winfo_reqheight() / 2 + initial_radius * scale)

            # 秒数カウントを更新
            for label, y_offset in labels:
                if "Total" in canvas.itemcget(label, 'text'):
                    canvas.itemconfig(label, text=f"Total Seconds: {elapsed_seconds}")
                if "Enlarge" in canvas.itemcget(label, 'text'):
                    canvas.itemconfig(label, text=f"Enlarge Seconds: {enlarge_seconds}")
                if "Stop" in canvas.itemcget(label, 'text'):
                    canvas.itemconfig(label, text=f"Stop Seconds: {stop_seconds}")
                if "Shrink" in canvas.itemcget(label, 'text'):
                    canvas.itemconfig(label, text=f"Shrink Seconds: {shrink_seconds}")

            window.update()
            time.sleep(0.01)  # タイムスリープ
            continue
        break


animation_thread = threading.Thread(target=animate_circle)
animation_thread.start()

def on_closing():
    global animation_running
    animation_running = False
    window.quit()



# ウィンドウの表示
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
window.destroy()