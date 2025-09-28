package org.example.backend.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    // 注册拦截器
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 添加JWT拦截器
        registry.addInterceptor(new JwtInterceptor())
                // 配置需要拦截的路径（/**表示拦截所有请求）
                .addPathPatterns("/api/user/roles/**")
                // 配置不需要拦截的路径（如登录接口）
                .excludePathPatterns("/login")
                .excludePathPatterns("/register")
                .excludePathPatterns("/guest");
    }
}
