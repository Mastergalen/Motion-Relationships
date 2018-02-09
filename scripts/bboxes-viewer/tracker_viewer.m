addpath('utils')

% For when the tracker script has been applied
threshold = 0.9;

data = fileread('-3K26M-m_00.json');

json = jsondecode(data);
json = json.annotations;


startFrame = 0;
% seq = load_sequence_color('../video-processor/tmp', 'frame_', 0, 149, 3, 'jpg');
seq = load_sequence_color('../video-processor/tmp', 'frame_', startFrame, 149, 3, 'jpg');

[~, ~, ~, frames] = size(seq);

for t = 1:frames
    img = seq(:, :, :, t);
    bboxes = json{startFrame + t};
    fh = figure('visible', 'off');
    imshow( img, 'border', 'tight' ); %//show your image
    hold on;
    for i = 1:size(bboxes, 1)
        box = bboxes(i, :);
        id = box(1);
        rectCoords = box(2:5);
        rectangle('Position', rectCoords, 'EdgeColor','r' );
        text(rectCoords(1), rectCoords(2) + 10, strcat('ID: ', num2str(id)))
    end
    
    frm = getframe( fh );
    seq(:, :, :, t) = im2double(frm.cdata);
end

implay(seq);

write_video(seq);