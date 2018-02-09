% For reviewing raw bounding box detections

threshold = 0.9;

data = fileread('-3K26M-m_00-bboxes.json');

json = jsondecode(data);


% seq = load_sequence_color('../video-processor/tmp', 'frame_', 0, 149, -1, 'jpg');
seq = load_sequence_color('../video-processor/tmp', 'frame_', 0, 10, -1, 'jpg');

[~, ~, ~, frames] = size(seq);

for t = 1:frames
    img = seq(:, :, :, t);
    bboxes = json{t};
    fh = figure('visible', 'off');
    imshow( img, 'border', 'tight' ); %//show your image
    hold on;
    if t == 82
        disp('hold on')
    end
    for i = 1:size(bboxes, 1)
        box = bboxes(i, :);
        confidence = box(5);
        if confidence < threshold
            continue
        end
        rectangle('Position', [box(1:2), (box(3) - box(1)),...
            (box(4) - box(2))], 'EdgeColor','r' );
    end
    
    frm = getframe( fh );
    seq(:, :, :, t) = im2double(frm.cdata);
end

implay(seq);