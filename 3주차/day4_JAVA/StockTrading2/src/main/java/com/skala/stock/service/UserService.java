package com.skala.stock.service;

import com.skala.stock.dto.UserDto;
import com.skala.stock.entity.User;
import com.skala.stock.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;

    @Transactional
    public UserDto createUser(UserDto userDto) {
        if (userRepository.existsByUsername(userDto.getUsername())) {
            throw new RuntimeException("이미 존재하는 사용자명입니다: " + userDto.getUsername());
        }
        if (userRepository.existsByEmail(userDto.getEmail())) {
            throw new RuntimeException("이미 존재하는 이메일입니다: " + userDto.getEmail());
        }

        User user = User.builder()
                .username(userDto.getUsername())
                .password(userDto.getPassword())
                .email(userDto.getEmail())
                .balance(userDto.getBalance())
                .build();

        User savedUser = userRepository.save(user);
        return convertToDto(savedUser);
    }

    public UserDto getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("사용자를 찾을 수 없습니다: " + id));
        return convertToDto(user);
    }

    public List<UserDto> getAllUsers() {
        return userRepository.findAll().stream()
                .map(this::convertToDto)
                .collect(Collectors.toList());
    }

    /** [CRUD 1] 사용자 수정 */
    @Transactional   // ★ 또 나왔죠? 데이터를 바꾸는 메서드의 필수품
    public UserDto updateUser(Long id, UserDto userDto) {
// 1단계: 수정 대상 찾기
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("사용자를 찾을 수 없습니다: " + id));

// 2단계: username 중복 검사 — "내가 지금 쓰는 이름 그대로"는 허용하고,
//         "다른 사람이 이미 쓰는 이름으로 변경"만 막는다
        if (!user.getUsername().equals(userDto.getUsername())          // 이름을 바꾸려는데
                && userRepository.existsByUsername(userDto.getUsername())) {  // 그 이름이 이미 있으면
            throw new RuntimeException("이미 존재하는 사용자명입니다: " + userDto.getUsername());
        }

// 3단계: 값 교체 후 저장
        user.setUsername(userDto.getUsername());
        user.setEmail(userDto.getEmail());
        user.setBalance(userDto.getBalance());
        User updatedUser = userRepository.save(user);
        return convertToDto(updatedUser);
    }

    /** [CRUD 2] 사용자 삭제 */
    @Transactional
    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {                 // 존재 확인 먼저 (PART 1과 동일 이유)
            throw new RuntimeException("사용자를 찾을 수 없습니다: " + id);
        }
        userRepository.deleteById(id);
    }
    private UserDto convertToDto(User user) {
        return UserDto.builder()
                .id(user.getId())
                .username(user.getUsername())
                .password(user.getPassword())
                .email(user.getEmail())
                .balance(user.getBalance())
                .build();
    }
}
