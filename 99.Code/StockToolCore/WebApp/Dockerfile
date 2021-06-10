FROM mcr.microsoft.com/dotnet/aspnet:5.0
RUN sed -i "s|DEFAULT@SECLEVEL=2|DEFAULT@SECLEVEL=1|g" /etc/ssl/openssl.cnf
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
EXPOSE 80
WORKDIR /app
#COPY . .
ENTRYPOINT ["dotnet", "WebApp.dll"]