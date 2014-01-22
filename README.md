JobSchedulerAbstractionSystem (JSAS)
------------------------------------

スーパーコンピュータなどに使われている各種ジョブスケジューラを、統一的な設定で使えるようにするソフトウェアを目指して開発継続中です。  
現在は、PJM(最近だと理研 京やFX10などに使われている)向けのいわゆるジョブスクリプトの、ごく簡易的なものを生成する機能のみです。  
需要がありそうなら将来的には、ssh接続でジョブを投げたり、データの送受信する機能などを追加しようと考えています。  
  
現在、複数のスーパーコンピュータを利用していたり、利用しようとしている人の協力やフィードバックを強く求めています。  


HELP
----

python jsas.py -h
