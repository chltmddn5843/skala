# Java Day 1 학습 정리

## 1. 오늘의 학습 목표

- 클래스와 객체의 차이를 이해한다.
- 생성자가 필요한 이유를 이해한다.
- `private`과 `public`의 역할을 구분한다.
- 상속(`extends`)의 의미를 이해한다.
- `static main()`이 프로그램의 시작점인 이유를 이해한다.

## 2. 클래스와 객체

클래스는 객체를 만들기 위한 **설계도**이고, 객체는 그 설계도로 만든 **실제 대상**이다.

```java
public class Product {
    private String name;
    private int price;
}
```

`Product`는 상품의 구조를 정의한 클래스다.

```java
Product apple = new Product("사과", 1000);
Product milk = new Product("우유", 2000);
```

`apple`과 `milk`는 `Product` 클래스로 만든 서로 다른 객체다. 같은 구조를 사용하지만 각자 다른 값을 가진다.

## 3. 생성자

생성자는 `new`로 객체를 만들 때 처음 실행되며, 객체의 초기값을 설정한다.

```java
public Product(String name, int price) {
    this.name = name;
    this.price = price;
}
```

생성자에는 다음 규칙이 있다.

- 생성자 이름은 클래스 이름과 정확히 같아야 한다.
- 대소문자도 같아야 한다.
- 반환 타입을 작성하지 않는다.

```java
public class Student {
    public Student(String name) {
        // 올바른 생성자
    }
}
```

`DiscountProuct`처럼 클래스 이름 `DiscountProduct`와 다르게 작성하면 생성자로 인식되지 않는다.

## 4. `static main()`

Java 프로그램은 다음 메서드에서 시작한다.

```java
public static void main(String[] args) {
    System.out.println("프로그램 시작");
}
```

- `public`: JVM이 클래스 외부에서 접근할 수 있다.
- `static`: JVM이 객체를 만들지 않고 호출할 수 있다.
- `void`: 반환값이 없다.
- `main`: JVM이 찾는 약속된 시작 메서드 이름이다.
- `String[] args`: 실행할 때 전달받는 문자열 목록이다.

메인 **클래스**가 `static`인 것이 아니라 `main()` **메서드**가 `static`이다.

## 5. `private`과 `public`

기본 원칙은 다음과 같다.

> 객체가 가진 데이터는 `private`으로 보호하고, 외부에 제공할 기능은 `public`으로 공개한다.

```java
public class Product {
    private String name;
    private int price;

    public int getPrice() {
        return price;
    }

    public void setPrice(int price) {
        if (price < 0) {
            throw new IllegalArgumentException("가격은 음수일 수 없습니다.");
        }

        this.price = price;
    }
}
```

`price`가 `public`이면 외부에서 음수 가격을 직접 저장할 수 있다. `private`으로 보호하고 `setPrice()`를 통하게 하면 값을 검사할 수 있다.

이처럼 객체가 자신의 데이터를 보호하고, 정해진 기능을 통해 사용하도록 만드는 것을 **캡슐화**라고 한다.

## 6. 상속

상속은 기존 클래스의 공통 데이터와 기능을 물려받아 새로운 클래스를 만드는 방법이다.

```java
public class DiscountProduct extends Product {
    private int rate;
}
```

위 코드는 다음 의미다.

> 할인 상품은 상품의 한 종류다.

상속 관계가 자연스러운지 확인하려면 **자식은 부모의 한 종류다**라는 문장이 성립하는지 확인한다.

```java
public class Dog extends Animal
```

이는 “개는 동물의 한 종류다”라는 뜻이다. 이러한 관계를 **IS-A 관계**라고 한다.

### 상속을 사용하는 이유

- 부모의 공통 데이터와 기능을 재사용할 수 있다.
- 같은 코드를 자식 클래스마다 반복하지 않아도 된다.
- 자식만의 데이터와 기능을 추가할 수 있다.
- 부모의 기능을 자식에 맞게 재정의할 수 있다.

## 7. `super`와 `@Override`

```java
public class DiscountProduct extends Product {
    private int rate;

    public DiscountProduct(String name, int price, int rate) {
        super(name, price);
        this.rate = rate;
    }

    @Override
    public int getPrice() {
        return super.getPrice() * (100 - rate) / 100;
    }
}
```

- `super(name, price)`: 부모인 `Product`의 생성자를 호출한다.
- `super.getPrice()`: 부모가 가진 원래 가격 조회 기능을 호출한다.
- `@Override`: 부모에게 물려받은 메서드를 자식에 맞게 다시 정의한다.

가격이 10,000원이고 할인율이 20%라면 다음과 같이 계산된다.

```text
10000 × (100 - 20) ÷ 100 = 8000
```

## 8. 현재 실습 코드의 목적

```java
Product normalItem = new Product("노말 아이템", 10000);
DiscountProduct discountItem =
        new DiscountProduct("할인 아이템", 10000, 20);

System.out.println(normalItem.getPrice());
System.out.println(discountItem.getPrice());
```

의도한 출력은 다음과 같다.

```text
10000
8000
```

일반 상품과 할인 상품은 모두 상품이지만, `getPrice()`의 동작은 서로 다르다는 것을 확인하는 실습이다.

## 9. 컴파일과 실행

Java 코드는 다음 순서로 실행된다.

```text
.java 소스 파일 → 컴파일 → .class 파일 생성 → JVM 실행
```

어떤 Java 파일에 문법 오류가 있으면 컴파일이 실패하고 `Main.class`가 만들어지지 않을 수 있다. 이때 실행하면 `ClassNotFoundException`이 발생할 수 있다.

현재 코드에서 확인했던 주요 수정 사항은 다음과 같다.

```java
// 상속 선언
public class DiscountProduct extends Product

// 생성자 이름은 클래스 이름과 동일
public DiscountProduct(...)

// 실제 반환값 price가 int이므로 반환 타입도 int
public int getPrice()
```

## 10. 복습 문제

1. 클래스와 객체의 차이는 무엇인가?
2. 생성자 이름은 무엇과 같아야 하는가?
3. `main()` 메서드가 `static`인 이유는 무엇인가?
4. 객체의 필드를 일반적으로 `private`으로 선언하는 이유는 무엇인가?
5. `DiscountProduct extends Product`를 우리말로 어떻게 읽을 수 있는가?
6. `super(name, price)`는 누구의 생성자를 호출하는가?
7. `@Override`는 언제 사용하는가?

## 11. 한 문장 요약

> 클래스는 객체의 설계도이고, 캡슐화는 객체의 데이터를 보호하며, 상속은 기존 클래스의 공통 기능을 물려받아 더 구체적인 클래스를 만드는 방법이다.
