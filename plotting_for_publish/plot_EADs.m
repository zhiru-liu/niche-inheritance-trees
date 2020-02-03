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

%% Plot EADs versus sigma
%std = [0, 1, 1.5, 2.0, 2.5, 3.0];
std = [0, 1.0, 2.0, 3.0];
inds = [0, 1, 3, 5];
shifts = [2, 1, 0, 0];
threshold = 10^3; %Remember to change the threshold
fig1 = figure; 
%fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off');
set(fig1,'PaperUnit','inches');
set(fig1,'PaperSize',[3.375 2.5]);
set(fig1,'PaperPositionMode','manual');
set(fig1,'PaperPosition',[0 0 3.375 2.5]);

hold on;
legent_ar = {};
for i = 4:-1:1
    ind = inds(i);
    shift = shifts(i);
    filename = ['/Users/Device6/Documents/Research/UIUC/nigel/tree/data/EADs/average/EAD_average_sigma_',int2str(ind),'.csv'];
    EAD_data = load(filename);
    k = EAD_data(:,1);
    S = EAD_data(:,2)*10^(shift);
    k_ = k(k<threshold); % Not plotting the noisy tail
    S_ = S(k<threshold);
    clear EAD_data;
    p1 = plot(k_, S_, '.');
    set(p1, 'markersize', 1);
    legend_ar{5-i} = sprintf('$\\sigma_%d=%1.1f$',i,std(i));
end

%% Plot two reference lines here
kk = logspace(1.3,2.3,100);
y = kk.^-2*10^(2.5);
y2 = kk.^-1*10^-4;
p2 = plot(kk, y);
p3 = plot(kk, y2);
set(p2, 'linewidth', 1);
set(p3, 'linewidth', 1);
legend_ar{5} = sprintf('$\\alpha=%d$',2);
legend_ar{6} = sprintf('$\\alpha=%d$',1);
%%%%%%%%%%%%%%%%%%%

hold off;
box on;
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');
ylabel('$S(k)$', 'interpreter', 'latex');
xlabel('$k$', 'interpreter', 'latex') ;
set(gca, 'XTick', (10.^(0:5)));
set(gca, 'YTickMode', 'auto');
set(gca, 'fontsize', 8);
leg = legend(legend_ar, 'Interpreter', 'latex');
set(leg, 'fontsize', 5, 'location', 'southwest');
legend boxoff;
legendmarkeradjust(5);
%% Print to file
filename = './results/temp/EADs_vs_sigmas.pdf';
print(filename,'-dpdf');
%filename = './results/temp/EADs_vs_sigmas_inset.png';
%print(filename, '-dpng', '-r600')