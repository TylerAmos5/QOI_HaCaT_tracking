#retrain a Cellpose model
"""
train a model using the labels from the GUI (_seg.npy)
by using the following option --mask_filter _seg.npy.

Ensure that the mask (filename_seg.npy) files are in the same directory 
as their initial images. Also, ensure that _seg.npy files match
the filename of the tiff files.
"""
python -m cellpose --train \
    --dir "C:/Users/laure/OneDrive - UCB-O365/Liu_images/training_data" \
    --pretrained_model nuclei --chan 2 --chan2 1 \
    --learning_rate 0.1 --weight_decay 0.0001 \
    --n_epochs 100 --mask_filter _seg.npy \
    --model_name_out "retrained_nuclei"

