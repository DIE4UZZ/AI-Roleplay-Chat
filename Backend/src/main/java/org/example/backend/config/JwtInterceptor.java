package org.example.backend.config;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.example.backend.common.constant;


@Component
public class JwtInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String authHeader = request.getHeader("Authorization");

        // 检查Token是否存在及格式是否正确
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, constant.INVALID_TOKEN);
            return false;
        }

        String token = authHeader.substring(7);
        try {
            Claims claims = Jwts.parser()
                    .setSigningKey(constant.SECRET)
                    .parseClaimsJws(token)
                    .getBody();

            String username = claims.get("username", String.class);
            Boolean loginStatus = claims.get("loginStatus", Boolean.class);

            if (loginStatus == null || !loginStatus) {
                response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "用户未登录");
                return false;
            }

            // 将用户信息存入请求属性
            request.setAttribute("username", username);
            request.setAttribute("loginStatus", loginStatus);

            return true;
        } catch (Exception e) {
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, constant.TOKEN_IS_WRONG);
        }

        return false;
    }
}


