clear all;

%% set default color order. %matlab only provides 7 colors then it'll repeat
co = [0    0.4470    0.7410;
    0.8500    0.3250    0.0980;
    0.9290    0.6940    0.1250;
    0.4940    0.1840    0.5560;
    0.4660    0.6740    0.1880;
    0.3010    0.7450    0.9330;
    0.6350    0.0780    0.1840;
    0.6471    0.3804    0.0510;
    0.7529    0.7765    0.0824;
    0.8471    0.3882    0.7098   
    ];
set(groot,'defaultAxesColorOrder',co);

%%%%%%%%%%%%%%%%%
%% Plot Niches versus sigma
% Fig S2
std = [0, 1, 1.5, 2.0, 2.5, 3.0];
lgR = 1;crs;
fig1 = figure; 
fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off');
set(fig1,'PaperUnit','inches');
set(fig1,'PaperSize',[3.375 2.5]);
set(fig1,'PaperPositionMode','manual');
set(fig1,'PaperPosition',[0 0 3.375 2.5]);

hold on;
legent_ar = {};
for i = 6:-1:1
    filename = ['../data/niche_saturation/niche_R_0=',int2str(lgR),'_',int2str(i-1)];
    data = load(filename);
    ind_ = downsample(data(:,1),1);
    niche_ = downsample(data(:,5), 1);
    clear data;
    p1 = plot(ind_, niche_, '.');
    set(p1, 'markersize', 1);
    legend_ar{7-i} = sprintf('$\\sigma_%d=%1.1f$',i,std(i));
end
hold off;
box on;
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');
ylim([10^-10 10^12])
ylabel('Niche', 'interpreter', 'latex');
xlabel('Index', 'interpreter', 'latex') ;
set(gca, 'XTickMode', 'auto');
set(gca, 'YTickMode', 'auto');
set(gca, 'fontsize', 7);
leg = legend(legend_ar, 'Interpreter', 'latex');
set(leg, 'fontsize', 5.5, 'location', 'southwest');
legend boxoff;
legendmarkeradjust(5);

filename = ['./results/saturation_R_0=','1'];
print(filename,'-dpng','-r600');