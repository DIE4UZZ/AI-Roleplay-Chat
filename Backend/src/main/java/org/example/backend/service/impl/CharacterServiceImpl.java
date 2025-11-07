package org.example.backend.service.impl;

import com.github.pagehelper.PageHelper;
import jakarta.servlet.http.HttpServletRequest;
import org.example.backend.mapper.CharacterMapper;
import org.example.backend.pojo.Character;
import org.example.backend.pojo.Result;
import org.example.backend.pojo.getCharacterResult;
import org.example.backend.service.CharacterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.example.backend.common.constant;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

@Service
public class CharacterServiceImpl implements CharacterService {

    @Autowired
    private CharacterMapper characterMapper;

    @Autowired
    private RedisTemplate redisTemplate;

    @Override
    public getCharacterResult getCharacter(String keyword, int page, int size) {
        if (keyword == null || keyword.length() == 0) {
            return getCharacterResult.error();
        }
        PageHelper.startPage(page, size);
        List<Character> character = characterMapper.getCharacter(keyword);
        if (character == null || character.size() == 0) {
            return getCharacterResult.error();
        }
        return getCharacterResult.success(character);
    }

    @Override
    public Result getBackground(int id) {
        if (id <= 0) {
            return Result.error("id不正确");
        }
        String background = characterMapper.getBackground(id);
        if (background == null || background.length() == 0) {
            return Result.success("角色不存在");
        }
        return Result.success(background);
    }

    @Override
    public Result saveCharacter(int roleId, HttpServletRequest request) {
        String username = (String) request.getAttribute("username");
        if (redisTemplate.opsForSet().isMember(username, roleId)) {
            return Result.success("重复收藏");
        }
        int characterId = roleId;
        int  insertSaveCharacterResult= characterMapper.insertSaveCharacter(username, characterId);
        if (insertSaveCharacterResult == 0) {
            return Result.error("添加失败");
        }
        redisTemplate.opsForSet().add(username, roleId);
        return Result.success();
    }

    @Override
    public Result getSaveCharacter(HttpServletRequest request) {
        String username = (String) request.getAttribute("username");
        Set<Integer> members = redisTemplate.opsForSet().members(username);
        List<Character> characterList = new ArrayList<>();
        for (Integer characterId : members) {
            Character characterById = characterMapper.getCharacterById(characterId);
            characterList.add(characterById);
        }
        return Result.success(characterList);
    }
}
