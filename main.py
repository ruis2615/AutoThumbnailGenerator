import os
import cv2
from datetime import datetime
from dotenv import load_dotenv

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

def process_videos_in_directory(input_dir, output_dir, times_in_seconds):
    """
    ディレクトリ内の全ての動画ファイルを処理する関数
    
    Parameters:
    input_dir (str): 入力ディレクトリのパス
    output_dir (str): 出力先ディレクトリのパス
    times_in_seconds (list): 抽出したい時間（秒）のリスト
    
    Returns:
    dict: 各動画ファイルごとの処理結果を含む辞書
    """
    results = {}
    
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
        
    times_to_extract = [20.0, 150.0, 180.0, 300.0]  # 抽出したい時間（秒）のリスト
    
    # 処理実行
    results = process_videos_in_directory(input_directory, output_directory, times_to_extract)
    
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