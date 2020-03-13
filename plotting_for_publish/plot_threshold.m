clear all;
% This script generates Fig. S3.

% file containing all EAD data for high R0
filename = '../data/threshold/R_0=9/EAD_sigma_4_rep_0.csv';

% file containing EAD data only in the fluctuation stage (see SI for more)
%filename = '../data/threshold/EAD_sigma_4_rep_0.csv';

fig1 = figure; 
%fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off');
set(fig1,'PaperUnit','inches');
set(fig1,'PaperSize',[3.375 2.5]);
set(fig1,'PaperPositionMode','manual');
set(fig1,'PaperPosition',[0 0 3.375 2.5]);

data = load(filename);
hold on;
threshold = 10^4;
k = data(:,1);
S = data(:,2);
k_ = k(k<threshold);
S_ = S(k<threshold);
p1 = plot(k_, S_, '.');
set(p1, 'markersize', 1);
% % Also add a reference line
% kk = logspace(1,3,100);
% y = kk.^-1.2*10^(-1.7);
% p2 = plot(kk, y,'r');
% hold off;
% leg = legend({'$\sigma=2.5$', 'Reference $\alpha=1.2$'}, 'Interpreter', 'latex');

box on;
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');
ylabel('$S(k)$', 'interpreter', 'latex');
xlabel('$k$', 'interpreter', 'latex') ;
set(gca, 'XTick', (10.^(0:2:6)));
set(gca, 'YTick', (10.^(-12:3:0)));
set(gca, 'fontsize', 7);

% set(leg, 'fontsize', 6, 'location', 'southwest');
legend boxoff;
% legendmarkeradjust(5);

filename = './results/sigma=25_R_0=9_no_threshold.pdf';
print(filename,'-dpdf');