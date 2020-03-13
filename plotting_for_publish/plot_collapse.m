clear all


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
set(groot,'defaultAxesColorOrder',co)

%%%%%%%%%%%%%%%%%

r_e = [0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001];
eta = 1.53; b = 0.36;
%% plot data collapsed C(A) versus r_epsilon
% Generates Fig 4

fig1 = figure; 
%fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off')
set(fig1,'PaperUnit','inches')
set(fig1,'PaperSize',[3.375 2.5])
set(fig1,'PaperPositionMode','manual')
set(fig1,'PaperPosition',[0 0 3.375 2.5])

hold on
legent_ar = {};
% Plot all the C(A) data
for i = 7:-1:1
    filename = ['../data/data_collapse/AC/AC_average_sigma=25_r_e_',int2str(i-1),'.csv'];
    AC_data = load(filename);
    A_ = AC_data(1:end,1);
    C_ = AC_data(1:end,2);
    r = r_e(i);
    x_ = r^b.*A_;
    clear AC_data
    p1 = plot(x_, C_./(A_.^eta), '.');
    set(p1, 'markersize', 1)
    legend_ar{8-i} = sprintf('$r_{\\epsilon%d}=%0.4f$',i,r_e(i));
end

x2_ = logspace(3, 5);
p2 = plot(x2_, log(x2_).*x2_.^(1-eta)*10^-0.1);
set(p2, 'linewidth', 1, 'color', 'r');
legend_ar{8} = sprintf('$x^{1-\\eta}\\mathrm{ln}(x)$');
%%
hold off
box on
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');
ylabel('$\bar{C}/{A^{\eta}}$', 'interpreter', 'latex')
xlabel('$x=r_{\epsilon}^{b} A$', 'interpreter', 'latex') 
title('$\eta=1.53, b=0.36$', 'interpreter', 'latex')
set(gca, 'XTick', (10.^(-2:6)));
set(gca, 'YTick', (10.^(-2:0)));
set(gca, 'fontsize', 7)
leg = legend(legend_ar, 'Interpreter', 'latex');
set(leg, 'fontsize', 6, 'location', 'southwest')
legend boxoff
% Call the helper function to adjust marker size
legendmarkeradjust(5)

filename = './results/collapse.pdf';
%print(filename,'-dpdf');
%}