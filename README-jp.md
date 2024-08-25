# Non-strict Attentional Region Annotation for Harvesting Image Databases

[English](README.md)

本データセットは一般画像データセットである [Harvesting Image Databases](https://www.robots.ox.ac.uk/~vgg/data/mkdb/index.html) に非厳密な領域アノテーション（Non-strict Attentional Region Annotation, NARA）を付与したものです．

NARA は単純な形状（楕円）のマーカでカテゴリ分類の際にアノテーション作業者が何処に注目したかの情報を示したもので，単純な操作で人間の認識の根拠となる情報を記録し，これを用いることでクラス分類モデルの認識精度を向上させるものです．

<img src="sample_images/blend_00001.png"
 alt="Example of blended image">

手法の詳細については以下の発表論文を参照してください．

> 荒井 敏, 白川 真一, 長尾 智晴,
> "非厳密な領域アノテーションによる畳み込みニューラルネットワークの一般画像分類精度の向上",
> FIT 2024 第 23 回情報科学技術フォーラム.

> Satoshi Arai, Shinichi Shirakawa, and Tomoharu Nagao,
> "Non-strict Attentional Region Annotation to Improve Image
> Classification Accuracy," IEEE SMC 2021.

## 画像データセット

アノテーションのベースとなる画像データセットは [Harvesting Image Databases](https://www.robots.ox.ac.uk/~vgg/data/mkdb/index.html) のサイトからダウンロードできます．

*18 Object-Class Databases* に列挙されている 18 クラスの zip ファイルをダウンロードし適当な場所に展開してください．
画像ファイル以外のメタファイルなども含まれていますがそれらは使用しません．

Harvesting Image Databases は Web から検索して収集した画像に基づいているため，カテゴリに相応しくない画像もノイズとして含まれています．
その様な画像は目視で（オリジナルのデータセットの段階で）仕分けされており，我々のアノテーション対象からも除外されています．
実際にアノテーションが付与された画像のファイル名は [harvestingdb_nara.csv](harvestingdb_nara.csv) の Image 列に記載されています．

## アノテーション結果

アノテーション結果は [harvestingdb_nara.csv](harvestingdb_nara.csv) に記録されており，各行が一つのアノテーションに対応しています．
このファイルにはアノテーション時の楕円マーカーの位置や大きさなどが数値データとして記録されています．
同一の画像に対して異なる３人の作業者がアノテーションを付与しているため，連続する３行がワンセットです．

本ファイルは CSV フォーマットで記録された表形式データであり，各列には以下の内容が記録されています．

| 列名 | 内容 |
|:-|:-|
| WorkTimeInSeconds | アノテーション作業時間（カテゴリ分類作業と領域アノテーション作業を合わせた秒数） |
| Image | 画像ファイル名（フォルダ名部分が正解カテゴリを表す） |
| Answer.anno_angle | 楕円マーカの角度（ラジアン単位） |
| Answer.anno_centx, Answer.anno_centy | 楕円マーカの中心位置 |
| Answer.anno_imght, Answer.anno_imgwd | 画像サイズ（画素数） |
| Answer.anno_scale | アノテーション用に画像を提示した際のスケール |
| Answer.anno_sizex, Answer.anno_sizey | 楕円マーカの半径 |
| Answer | アノテーション作業者によるカテゴリ分類結果（正解カテゴリとは異なる分類がなされている場合があります） |

## アノテーションマップ生成スクリプト

アノテーション結果は楕円マーカ―の位置や大きさなどを数値データとして記録したものなので，実際に使用する際はこれを二次元画像に変換したすることを想定しています．
この変換を行うスクリプトとして [draw_annotation_maps.py](draw_annotation_maps.py) を提供しています．

requirements.txt に従って必要なパッケージをインストールした後，以下のコマンドを実行してください．
maps フォルダ以下にアノテーションマップが生成されます．

```python
python draw_annotation_maps.py --input_name harvestingdb_nara.csv --output_dir maps
```

<img src="sample_images/map_00001.png"
 alt="Example of annotation map">

## 特記事項

アノテーションを付与した画像のうち下記ファイルにはデータ破損が見られます．
画像ローダーによってはクラッシュする可能性がありますので適宜除外するなどしてください．
（例：PIL で読み込もうとするとエラーになります）

- bike/img_f1998e4035c3c9e73a7f5e29b98cb3e0efc2603d.png

## ライセンス

本アノテーション結果の使用に際しては[LICENSE](LICENSE.txt)が適用されます．

また Harvesting Image Databases に含まれる画像データについてはオリジナルの[LICENSE](https://www.robots.ox.ac.uk/~vgg/data/mkdb/LICENSE.TXT)を参照してください．

## 謝辞

この成果は，国立研究開発法人新エネルギー・産業技術総合開発機構(NEDO)の委託業務(JPNP20001221-0)の結果得られたものです．
