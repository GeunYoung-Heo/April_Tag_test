import cv2
import datetime

def capture_camera_feed():
    """
    USB 카메라로부터 비디오 스트림을 읽어와 화면에 표시하며,
    'c' 키 또는 마우스 클릭으로 캡처하고, '+'와 '-' 키로 Exposure(노출)을 조절하는 함수
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("오류: 카메라를 열 수 없습니다.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    
    initial_exposure = -6.0
    cap.set(cv2.CAP_PROP_EXPOSURE, initial_exposure)

    # ================================================================= #
    # ★★★★★ 1. 캡처 로직을 별도 함수로 분리 ★★★★★
    # ================================================================= #
    def save_current_frame(frame_to_save, trigger_source="키보드"):
        """현재 프레임을 파일로 저장하는 함수"""
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{now}.png"
        cv2.imwrite(filename, frame_to_save)
        print(f"'{trigger_source}' 입력으로 캡처 성공! 파일 저장: {filename}")

    # ================================================================= #
    # ★★★★★ 2. 마우스 콜백 함수 정의 ★★★★★
    # ================================================================= #
    # 메인 루프와 공유할 플래그 변수
    mouse_capture_requested = False

    def mouse_callback(event, x, y, flags, param):
        """마우스 이벤트가 발생할 때 호출될 함수"""
        nonlocal mouse_capture_requested
        # 왼쪽 마우스 버튼을 눌렀을 때 이벤트 감지
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse_capture_requested = True

    # ================================================================= #
    # ★★★★★ 3. 창을 만들고 콜백 함수 연결 ★★★★★
    # ================================================================= #
    window_name = 'Arducam Camera Feed'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    print("카메라 스트리밍을 시작합니다.")
    print("  - 마우스 클릭 또는 'c' 키: 현재 화면 캡처")
    print("  - '+' 키: 밝게 (노출 증가)")
    print("  - '-' 키: 어둡게 (노출 감소)")
    print("  - 'q' 키: 종료")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽어오지 못했습니다. 스트림 종료.")
            break

        display_frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)

        current_exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
        text = f"Exposure: {current_exposure:.2f}"
        cv2.putText(display_frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow(window_name, display_frame)

        # 키 입력 처리
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        
        # ================================================================= #
        # ★★★★★ 4. 키보드 또는 마우스 입력에 따른 캡처 실행 ★★★★★
        # ================================================================= #
        # 'c' 키를 누르거나, 마우스 클릭 요청이 있었을 경우
        if key == ord('c') or mouse_capture_requested:
            source = "마우스" if mouse_capture_requested else "키보드"
            # 고화질 원본 'frame'을 저장하는 함수 호출
            save_current_frame(frame, trigger_source=source)
            # 마우스 요청 플래그 초기화
            mouse_capture_requested = False
            
        elif key == ord('+') or key == ord('='):
            new_exposure = cap.get(cv2.CAP_PROP_EXPOSURE) + 1.0
            cap.set(cv2.CAP_PROP_EXPOSURE, new_exposure)
            print(f"Set new exposure to: {new_exposure:.2f}")
        elif key == ord('-'):
            new_exposure = cap.get(cv2.CAP_PROP_EXPOSURE) - 1.0
            cap.set(cv2.CAP_PROP_EXPOSURE, new_exposure)
            print(f"Set new exposure to: {new_exposure:.2f}")

    cap.release()
    cv2.destroyAllWindows()
    print("카메라 스트리밍이 종료되었습니다.")

if __name__ == "__main__":
    capture_camera_feed()