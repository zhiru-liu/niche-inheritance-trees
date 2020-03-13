clear all;
% This script generates figure S1

filename = '../data/probability/probability.txt';
fig1 = figure; 
%fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off');
set(fig1,'PaperUnit','inches');
set(fig1,'PaperSize',[3.375 2.5]);
set(fig1,'PaperPositionMode','manual');
set(fig1,'PaperPosition',[0 0 3.375 2.5]);

prob_data = load(filename);
sigmas = prob_data(:,1);
probs = prob_data(:,2);
p1 = plot(sigmas, probs, '.');
set(p1, 'markersize', 10);
hold on;
% Plot a reference poly fit
p = polyfit(sigmas, probs, 4);
v = polyval(p, sigmas);
plot(sigmas, v);
hold off;

box on;
ylabel('$P$', 'interpreter', 'latex');
xlabel('$\sigma$', 'interpreter', 'latex') ;
set(gca, 'XTickMode', 'auto');
set(gca, 'YTickMode', 'auto');
set(gca, 'fontsize', 7);

leg = legend({'Averaged probability', 'Interpolation'}, 'Interpreter', 'latex');
set(leg, 'fontsize', 6, 'location', 'southwest');
legend boxoff;
%legendmarkeradjust(5);

filename = 'plotting/results/percolation_probs.pdf';
print(filename,'-dpdf');