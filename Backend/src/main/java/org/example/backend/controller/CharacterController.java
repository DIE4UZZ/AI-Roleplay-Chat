package org.example.backend.controller;


import jakarta.servlet.http.HttpServletRequest;
import org.example.backend.pojo.Result;
import org.example.backend.pojo.getCharacterResult;
import org.example.backend.service.CharacterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class CharacterController {

    @Autowired
    private CharacterService characterService;

    //查询角色
    @GetMapping("/roles")
    public getCharacterResult getCharacter(@RequestParam(required = false) String keyword,
                                           @RequestParam(defaultValue = "1") int page,
                                           @RequestParam(defaultValue = "10") int size) {
        return characterService.getCharacter(keyword, page, size);
    }

    @GetMapping("/roles/{id}")
    public Result getBackground(@PathVariable int id) {
        return characterService.getBackground(id);
    }

    @GetMapping("/user/roles/{roleId}")
    public Result saveCharacter(@PathVariable int roleId, HttpServletRequest request) {
        return characterService.saveCharacter(roleId, request);
    }

    @GetMapping("/user/roles")
    public Result getSaveCharacter(HttpServletRequest request) {
        return characterService.getSaveCharacter(request);
    }
}
