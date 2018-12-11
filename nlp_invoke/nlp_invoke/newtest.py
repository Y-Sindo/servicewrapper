!python -m CopyNet.nmt.nmt.nmt \
    --copynet \
    --attention=scaled_luong \
    --attention_architecture=standard \
    --optimizer=adam \
    --learning_rate=0.001 \
    --decay_scheme=luong10 \
    --src=in --tgt=out \
    --vocab_prefix=./dataset/api_match/voc \
    --train_prefix=./dataset/api_match/train \
    --dev_prefix=./dataset/api_match/dev \
    --test_prefix=./dataset/api_match/test \
    --out_dir=./results/CopyNet_0 \
    --num_train_steps=12000 \
    --steps_per_stats=100 \
    --steps_per_external_eval=500 \
    --num_layers=2 \
    --num_units=128 \
    --dropout=0 \
    --metrics=accuracy \
    --share_vocab=True \

#     --beam_width=10 \
#     --encoder_type=bi \