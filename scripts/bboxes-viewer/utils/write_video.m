function write_video( sequence )
%WRITE_VIDEO Summary of this function goes here
%   Detailed explanation goes here
disp('Writing video');
[~, ~, ~, frames] = size(sequence);

outputVideo = VideoWriter(fullfile('','tracked.mp4'), ...
    'MPEG-4');
outputVideo.FrameRate = 20.97;
open(outputVideo)

for t = 1:frames
   img = sequence(:, :, :, t);
   img = im2uint8(img);
   writeVideo(outputVideo, img);
end

end
