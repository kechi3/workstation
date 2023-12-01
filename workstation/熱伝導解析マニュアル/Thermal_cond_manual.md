<style>  
  hr {  
    opacity: 0;  
    break-after: page;  
  }  
</style>  

#  熱伝導解析@openfoam
- CADでastファイルを作る
    1. スケッチを作成
![すてきな画像](cad1.png)
    1. ①四角形を描画②横幅調整③縦幅調整④中心との距離調整
![すてきな画像](cad2.png)
    1. スケッチを押し出してソリッドを作成
![すてきな画像](cad3.png)
    1. ソリッドからサーフェスを作成(下矢印ボタンを2回押す)
![すてきな画像](cad4.png)
    1. fileメニューからサーフェスをastファイルとして出力(複数一括出力もOK)
![すてきな画像](cad5.png)
    1. この後は部分ごとにメッシュを作成するケースについて説明  
    1. astファイルを部分ごとにわけて保存(ここではupとdown)  
![すてきな画像](cad6.png)
    1. astファイル内のMeshの部分を任意のサーフェス名に置換 
![すてきな画像](cad7.png)
- stlファイルの準備
    1. astファイルを一つにまとめる
![すてきな画像](cad8.png)
    1. cadは寸法がmmで設定されているため、mに変換(openfoamの機能を使用)
![すてきな画像](cad9.png)
![すてきな画像](cad10.png)
    1. 特徴線を抽出する(綺麗にメッシュが切れるようになる操作という理解でOK)
![すてきな画像](cad11.png)
- メッシュを作成
    1. system/meshDictを編集し、対象のfmsファイルを選択、メッシュサイズを設定
![すてきな画像](cad12.png)
    1. 任意のメッシャーでメッシュを作成(今回はpMesh)
![すてきな画像](cad13.png)
    1. 個別のメッシュをマージ①マージ対象のメッシュ情報を移動②マージコマンドを実行
![すてきな画像](cad14.png)
- 解析条件を設定
    1. 壁面タイプを設定 今回は全てWall outletとinletはpatchでも良い<br>file:constant/polyMesh/boundary
![すてきな画像](case15.png)
    1. 境界条件を設定<br>file:0/T
![すてきな画像](cad16.png)
- 解析を実行する<br>今回はlaplacianFoam
- 解析結果を可視化<br>command:foamToVTK
 



---


