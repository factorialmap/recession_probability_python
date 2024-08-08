# packages    ----------------------------------------------------------------------------------------------
library(quantmod)


# data   ----------------------------------------------------------------------------------------------
#curva de juros 10 vs 2 anos
getSymbols("T10Y3M", src="FRED")

#periodos de recessao
getSymbols("USREC", src="FRED")


# explore   ----------------------------------------------------------------------------------------------

#Como está a curva de juros ?
chartSeries(T10Y3M, type = c("line"), theme = "black")

#Quantos registros ?
length(USREC)
length(T10Y3M)  

#Qual a unidade temporal ?
head(USREC)
head(T10Y3M)


# pre processing  ----------------------------------------------------------------------------------------------

#reduzindo pontos de observacao da curva
yield_curve <- T10Y3M[xts:::startof(T10Y3M, "months")]
head(yield_curve)
length(yield_curve)

#reduzindo intervalo da curva
yield_curve <- yield_curve["1985::2022"]

#reduzindo intervalo da recessao
recession <- USREC["1985::2022"]

head(yield_curve)
head(recession)

length(yield_curve)
length(recession)  

#juntando os dados
dados <- merge(yield_curve,recession)

#os dados estao ai mas sabemos que a recessao vem 6 a 12 meses depois da curva de juros e nao no momento exato
head(dados,15)

#teremos que atrazar a curva de juros, vou atrazar em 6 meses
dados_6 <- lag(yield_curve,6)

dados_6

tail(yield_curve)
tail(dados_6)

#juntar dados novamente
dados_minus_6_months <- 
  merge(dados_6, recession)

tail(dados_minus_6_months)

#houve problema durante a juncao dos dados mes 12 repetiu 2x ou seja, dois dias no mes 12
dados_6 <- dados_minus_6_months[xts:::startof(dados_minus_6_months, "months")]

tail(dados_6)

#Vamos checar quantos dados nulos...me parece 150
summary(dados_6)


#Criando funÃ§Ã£o para preencher os dados nulos
for(i in 1:length(dados_6[,1])){ #iterating through dates
  date = index(dados_6)[i] #"date" is current date
  dados_6[i, 1] = ifelse( 
    is.na( dados_6[i,1] ) == TRUE, #Test if the value is NA
    T10Y3M[date-1], #If it is NA, grab the yield curve data from the day before
    dados_6[i,1] #Otherwise, keep today's value
  )
}
length(which(is.na(dados_6[,1])==TRUE)) # How many are NA now?

# Ainda 67 dados nulos
summary(dados_6)


#Let's run again
for(i in 1:length(dados_6[,1])){
  date = index(dados_6)[i]
  dados_6[i, 1] = ifelse(
    is.na( dados_6[i,1] ) == TRUE,
    T10Y3M[date-3], #Only change, now get value from 3 days before
    dados_6[i,1]
  )
}
length(which(is.na(dados_6[,1])==TRUE)) # How many are NA now?
# I got 5

summary(dados_6)
#tem 5 dados nulos

#Run again
for(i in 1:length(dados_6[,1])){
  date = index(dados_6)[i]
  dados_6[i, 1] = ifelse(
    is.na( dados_6[i,1] ) == TRUE,
    T10Y3M[date-5], #Only change, now get value from 5 days before
    dados_6[i,1]
  )
}
length(which(is.na(dados_6[,1])==TRUE)) # How many are NA now?
# I got 0

summary(dados_6)
#tem 0 dados nulos

#Dar uma lida novamente nos dados
head(dados_6)
tail(dados_6)

#Primeiro, vou dividir os dados em um conjunto de treinamento e um conjunto de testes. 
#Eu gostaria de ver se poderÃ­amos prever a recessÃ£o de 2008 fora da amostra, entÃ£o eu vou executar 
#o conjunto de treinamento de 1985 a 2002, em seguida, o conjunto de testes serÃ¡ de 2002 a 2019.


#Separando os dados de treino e dados de teste
train_set <- dados_6["1985::2002"]
test_set  <- dados_6["2003::2022"]

#Treinando com regressÃ£o logÃ­stica a recesssion como variÃ¡vel Y dependente
#Contra a curva de juros que Ã© a variÃ¡vel X independente ou preditora
#model <- glm(train_set[,2] ~ train_set[,1],
#            family = binomial(link = "logit"))

model <- glm(USREC ~ T10Y3M, data = train_set, family = binomial(link = "logit") )

#Vamos ver os resultados
summary(model)

#Agora, podemos pegar os betas e inseri-los em nosso modelo de probabilidade. TENHA CUIDADO AQUI!
#NÃ£o Ã© tÃ£o simples quanto vocÃª pode esperar inicialmente. Lembre-se de que os betas e as variÃ¡veis
#independentes estÃ£o no expoente. Isso significa que vocÃª precisa converter seu valor Y para
#gerar uma probabilidade:

model$coefficients[2]

#Converter o valor de Y
prob_recessao <- function(X, model) {
  Y <- model$coefficients[1] + model$coefficients[2]*X
  prob = 1/(1+exp(-Y))
  return(prob)
}

#Vamos executar nossos dados de teste por meio dele agora que o modelo Ã© treinado.
#Eu tambÃ©m quero plotar os dados para fazer uma inspeÃ§Ã£o visual.
prob_recessao_teste <- prob_recessao(test_set[,1], model )
plot(prob_recessao_teste, type="l", col="blue", main = "Probabilidade de recessão nos Estados Unidos")


data_rec <- data.frame(date = index(prob_recessao_teste), coredata(prob_recessao_teste))

library(ggplot2)

ggplot(data_rec,
       aes(x=date, y=T10Y3M)) +
  geom_line(size=1) +
  scale_x_date(breaks = "2 years", date_labels ="%Y") +
  scale_y_continuous(labels = scales::percent) +
  ggthemes::theme_fivethirtyeight() +
  annotate("rect", 
           xmin = as.Date("2007-12-01"),
           xmax = as.Date("2009-06-01"),
           ymin = -Inf,
           ymax = Inf,  
           fill = "#2dba92",
           alpha=.6) +
  annotate("rect", 
           xmin = as.Date("2020-02-01"),
           xmax = as.Date("2020-04-30"),
           ymin = -Inf,
           ymax = Inf,  
           fill = "#2dba92",
           alpha=.6)+
  
  labs(title = "Recession probability estimates",
       subtitle = "in %",
       caption = "country: USA, data source: FRED,inverted yield curve 10Y3M| Marcelo C. Anjos")





# help material -----------------------------------------------------------
tq_mutate_fun_options() 

source: https://www.business-science.io/timeseries-analysis/2017/08/30/tidy-timeseries-analysis-pt-4.html


xts:::startof()
https://stackoverflow.com/questions/22592193/r-xts-get-the-first-dates-and-values-for-each-month-from-a-daily-time-series