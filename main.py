import os
import cv2
from datetime import datetime
from dotenv import load_dotenv

def parse_time_str(time_str):
    """
    時間文字列を秒数に変換する関数
    
    Parameters:
    time_str (str): "1:7:40"や"1:8"、"30"、"3m"、"1h"などの時間文字列
    
    Returns:
    float: 秒数
    """
    # h,m,s指定の場合の処理
    if any(unit in time_str.lower() for unit in ['h', 'm', 's']):
        time_str = time_str.lower()
        total_seconds = 0.0
        
        # 時間(h)の処理
        if 'h' in time_str:
            hours = float(time_str.split('h')[0])
            total_seconds += hours * 3600
            time_str = time_str.split('h')[1]
            
        # 分(m)の処理
        if 'm' in time_str:
            minutes = float(time_str.split('m')[0])
            total_seconds += minutes * 60
            time_str = time_str.split('m')[1]
            
        # 秒(s)の処理
        if 's' in time_str:
            seconds = float(time_str.split('s')[0])
            total_seconds += seconds
            
        return total_seconds
    
    # 従来の時:分:秒形式の処理
    parts = time_str.split(':')
    if len(parts) == 3:  # 時:分:秒
        hours, minutes, seconds = map(float, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:  # 分:秒
        minutes, seconds = map(float, parts)
        return minutes * 60 + seconds
    else:  # 秒のみ
        return float(parts[0])

def extract_frames_from_video(video_path, times_in_seconds, output_dir):
    """
    動画から指定された複数の時間のフレームを抽出する関数
    
    Parameters:
    video_path (str): 動画ファイルのパス
    times_in_seconds (list): 抽出したい時間（秒）のリスト
    output_dir (str): 出力先ディレクトリ
    
    Returns:
    list: 保存された画像のパスのリスト
    """
    saved_paths = []
    try:
        # 動画を読み込む
        cap = cv2.VideoCapture(video_path)
        
        # 動画が正しく開けたか確認
        if not cap.isOpened():
            print(f"エラー: 動画ファイルを開けませんでした - {video_path}")
            return saved_paths
        
        # 動画のFPSを取得
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 動画の総フレーム数を取得
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 動画の長さ（秒）を計算
        video_duration = total_frames / fps
        
        # 動画ファイル名（拡張子なし）を取得
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # 動画ファイル用の出力ディレクトリを作成
        video_output_dir = os.path.join(output_dir, video_name)
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)
        
        # 各時間についてフレームを抽出
        for time_in_seconds in sorted(times_in_seconds):
            # 指定時間が動画の長さを超えている場合はスキップ
            if time_in_seconds > video_duration:
                print(f"指定された時間 {time_in_seconds}秒が動画の長さ {video_duration:.2f}秒を超えています - {video_path}")
                continue
            
            # フレーム番号を計算
            frame_number = int(fps * time_in_seconds)
            
            # フレーム位置を設定
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            # フレームを読み込む
            ret, frame = cap.read()
            
            if ret:
                # 出力ファイル名を生成（タイムスタンプと指定時間を含む）
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{video_name}_{timestamp}_time{time_in_seconds:.1f}s.jpg"
                output_path = os.path.join(video_output_dir, output_filename)
                
                # フレームを画像として保存
                cv2.imwrite(output_path, frame)
                
                print(f"フレームを保存しました：{output_path}")
                saved_paths.append(output_path)
        
        return saved_paths
    
    finally:
        # リソースを解放
        cap.release()

def process_videos_in_directory(input_dir, output_dir, time_strings):
    """
    ディレクトリ内の全ての動画ファイルを処理する関数
    
    Parameters:
    input_dir (str): 入力ディレクトリのパス
    output_dir (str): 出力先ディレクトリのパス
    time_strings (list): 抽出したい時間の文字列のリスト（例: ["1:7:40", "1:8", "30"]）
    
    Returns:
    dict: 各動画ファイルごとの処理結果を含む辞書
    """
    results = {}
    
    # 時間文字列を秒数に変換
    times_in_seconds = [parse_time_str(t) for t in time_strings]
    
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # サポートする動画フォーマット
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    
    # ディレクトリを再帰的に走査
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(video_extensions):
                video_path = os.path.join(root, file)
                try:
                    saved_paths = extract_frames_from_video(video_path, times_in_seconds, output_dir)
                    results[video_path] = {
                        'success': True,
                        'saved_frames': saved_paths
                    }
                except Exception as e:
                    print(f"動画の処理中にエラーが発生しました：{video_path}: {str(e)}")
                    results[video_path] = {
                        'success': False,
                        'error': str(e)
                    }
    
    return results

# 使用例
if __name__ == "__main__":
    # .envファイルから環境変数を読み込む
    load_dotenv()
    
    # .envファイルから入力・出力ディレクトリを読み込む
    input_directory = os.getenv('INPUT_DIRECTORY')
    output_directory = os.getenv('OUTPUT_DIRECTORY')
    
    if not input_directory or not output_directory:
        print("エラー：.envファイルにINPUT_DIRECTORYとOUTPUT_DIRECTORYを設定する必要があります")
        exit(1)
        
    # .envファイルから抽出時間のリストを読み込む
    time_strings_env = os.getenv('EXTRACT_TIMES', "20,2:30,3m,5m")  # デフォルト値を設定
    time_strings = [t.strip() for t in time_strings_env.split(',')]
    
    # 処理実行
    results = process_videos_in_directory(input_directory, output_directory, time_strings)
    
    # 処理結果の表示
    print("\n処理結果：")
    for video_path, result in results.items():
        print(f"\n動画：{video_path}")
        if result['success']:
            print(f"{len(result['saved_frames'])}個のフレームの抽出に成功しました")
            for frame_path in result['saved_frames']:
                print(f"  - {frame_path}")
        else:
            print(f"失敗：{result['error']}")